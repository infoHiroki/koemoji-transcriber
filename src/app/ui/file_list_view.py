import flet as ft
from typing import Callable, Dict, List, Optional
from flet import (
    Column,
    Row,
    Text,
    ListView,
    IconButton,
    TextButton, # Add TextButton
    icons,
    Container,
    alignment,
    border_radius,
    padding,
    margin,
    border,
    GestureDetector, # Added for click detection
    ListTile,
    Dropdown,    # Added for language selection
    dropdown,    # Added for language options
    # colors, # Use ft.colors instead
    border,      # Added for item border
    colors,      # Added for item background
)
import os
import logging # Added for logging

# --- Data structure to hold file info (instead of FileItem class) ---
class FileInfo:
    def __init__(self, path: str):
        self.path = path
        self.name = os.path.basename(path)
        self.status = "待機中"
        self.status_color = ft.colors.GREY
        self.language = "ja" # Default language
        self.processing_time_str: Optional[str] = None # To store formatted processing time
        self.result_text: Optional[str] = None
        self.timestamped_text: Optional[str] = None
        # References to UI controls within the Row/Container for updates
        self.ui_control: Optional[ft.Container] = None # Changed type hint
        self.status_text_control: Optional[ft.Text] = None
        self.time_text_control: Optional[ft.Text] = None
        self.language_dropdown_control: Optional[ft.Dropdown] = None

# --- Global state (managed within this module or passed around) ---
# This replaces the state previously held within FileListView instance
file_data: Dict[str, FileInfo] = {}
selected_file_path: Optional[str] = None
list_view_control: Optional[ft.ListView] = None
# clear_all_button_control: Optional[ft.TextButton] = None # Moved to main.py
on_select_callback: Optional[Callable[[Optional[FileInfo]], None]] = None
on_list_change_callback: Optional[Callable[[bool], None]] = None # Callback for list empty/not empty status

# --- UI Creation Function ---
def create_file_list_view(
    select_callback: Callable[[Optional[FileInfo]], None],
    list_change_callback: Callable[[bool], None] # Add callback parameter
) -> ft.ListView: # Return ListView directly
    """Creates the file list view UI components."""
    global list_view_control, on_select_callback, on_list_change_callback
    on_select_callback = select_callback
    on_list_change_callback = list_change_callback # Store the callback
    list_view_control = ft.ListView(expand=True, spacing=0, auto_scroll=True, padding=0)

    # Clear button creation moved to main.py

    # Return only the ListView control
    return list_view_control

# --- Helper Functions to manage state and UI ---

# --- Language Options ---
# Define language options centrally
LANGUAGE_OPTIONS = [
    dropdown.Option("ja", "日本語"), # Japanese text
    dropdown.Option("en", "英語"), # Japanese text
    dropdown.Option("zh", "中国語"), # Japanese text
    dropdown.Option("ko", "韓国語"), # Japanese text
    dropdown.Option("es", "スペイン語"), # Japanese text
    dropdown.Option("fr", "フランス語"), # Japanese text
    dropdown.Option("de", "ドイツ語"), # Japanese text
    # Add more as needed
]

def _handle_language_change(e):
    """Callback when a language dropdown value changes."""
    selected_language = e.control.value
    file_path = e.control.data # Get the file path stored in the dropdown's data
    if file_path in file_data:
        file_data[file_path].language = selected_language
        logging.info(f"Language for '{file_data[file_path].name}' set to: {selected_language}")
    else:
        logging.warning(f"Could not find file data for path '{file_path}' during language change.")

def _create_file_item_row(file_info: FileInfo) -> ft.Container: # Renamed function and return type
    """Creates a Container with a Row representing a file item."""
    # Create controls and store references in FileInfo
    file_info.status_text_control = ft.Text(
        file_info.status, size=14, color=file_info.status_color, weight=ft.FontWeight.NORMAL, width=60, no_wrap=True # Increased size by 2
    )
    file_info.time_text_control = ft.Text(
        file_info.processing_time_str or "", size=14, color=ft.colors.SECONDARY, visible=bool(file_info.processing_time_str), width=60 # Increased size by 2
    )
    file_info.language_dropdown_control = ft.Dropdown(
        options=LANGUAGE_OPTIONS,
        value=file_info.language,
        dense=True,
        text_size=14, # Increased size by 2
        # scale=1.0, # Remove scale
        content_padding=padding.symmetric(vertical=0, horizontal=5), # Adjust padding
        alignment=alignment.center_left,
        width=100, # Keep fixed width
        data=file_info.path, # Store file path to identify which file's language changed
        on_change=_handle_language_change,
    )

    delete_button = ft.IconButton(
            ft.Icons.DELETE_OUTLINE,
            tooltip="ファイルを削除",
            data=file_info.path,
            on_click=_handle_delete_click,
            icon_size=18 # Adjusted size
        )

    file_item_row = ft.Row(
        controls=[
            ft.Text(file_info.name, expand=True, weight=ft.FontWeight.BOLD, size=16), # Increased size by 2
            file_info.status_text_control,
            file_info.time_text_control,
            file_info.language_dropdown_control,
            delete_button,
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    container = ft.Container(
        content=file_item_row,
        padding=padding.symmetric(vertical=4, horizontal=8), # Add padding to container
        border_radius=border_radius.all(4),
        ink=True, # Add ink effect on click
        on_click=_handle_select_click,
        data=file_info.path,
        bgcolor=ft.colors.SECONDARY_CONTAINER if selected_file_path == file_info.path else None,
    )

    file_info.ui_control = container # Store reference to the container
    return container

def _handle_delete_click(e):
    """Callback for delete button click."""
    file_path = e.control.data
    remove_file(file_path)

def _handle_select_click(e):
    """Callback for ListTile click (selection)."""
    global selected_file_path
    file_path = e.control.data
    previous_selected_path = selected_file_path

    if selected_file_path == file_path: # Clicked already selected item - deselect? (Optional)
        # selected_file_path = None
        pass # Keep selected for now
    else:
        selected_file_path = file_path

    # Update UI for previous selection (if any) - Update Container bgcolor
    if previous_selected_path and previous_selected_path in file_data:
        prev_control = file_data[previous_selected_path].ui_control
        if prev_control:
            prev_control.bgcolor = None
            prev_control.update()

    # Update UI for new selection - Update Container bgcolor
    if selected_file_path and selected_file_path in file_data:
        new_control = file_data[selected_file_path].ui_control
        if new_control:
            new_control.bgcolor = ft.colors.SECONDARY_CONTAINER
            new_control.update()

    # Call the main callback
    if on_select_callback:
        selected_info = file_data.get(selected_file_path)
        on_select_callback(selected_info)

# Remove _update_clear_button_visibility as it's handled externally now
# def _update_clear_button_visibility(): ...

def add_files(file_paths: List[str]):
    """Adds files to the internal state and updates the UI."""
    global list_view_control
    if not list_view_control: return
    added_count = 0
    for path in file_paths:
        if path not in file_data:
            file_info = FileInfo(path)
            file_data[path] = file_info
            item_row = _create_file_item_row(file_info) # Use new function
            list_view_control.controls.append(item_row) # Add the container
            added_count += 1
    if added_count > 0:
        if list_view_control.page:
            list_view_control.update()
        # Notify about list change (not empty)
        if on_list_change_callback:
            on_list_change_callback(False) # False means not empty

def remove_file(file_path: str):
    """Removes a file from the internal state and updates the UI."""
    global list_view_control, selected_file_path
    if not list_view_control: return
    if file_path in file_data:
        file_info = file_data[file_path]
        if file_info.ui_control in list_view_control.controls:
            list_view_control.controls.remove(file_info.ui_control)
        del file_data[file_path]

        if selected_file_path == file_path:
            selected_file_path = None
            if on_select_callback: on_select_callback(None) # Notify deselection

        if list_view_control.page:
            list_view_control.update()
        # Notify about list change (potentially empty)
        if on_list_change_callback:
             on_list_change_callback(len(list_view_control.controls) == 0)

def clear_all_files():
    """Removes all files from the state and UI."""
    global list_view_control, file_data, selected_file_path
    if not list_view_control: return
    list_view_control.controls.clear()
    file_data.clear()
    selected_file_path = None
    if on_select_callback: on_select_callback(None) # Notify deselection
    if list_view_control.page:
        list_view_control.update()
    # Notify about list change (empty)
    if on_list_change_callback:
        on_list_change_callback(True) # True means empty

def update_file_status(
    file_path: str,
    new_status: str,
    color: str = ft.colors.GREY,
    processing_time_sec: Optional[float] = None
):
    """Updates the status and optionally processing time of a file in the state and UI."""
    if file_path in file_data:
        file_info = file_data[file_path]
        file_info.status = new_status
        file_info.status_color = color if color else ft.colors.GREY

        # Update processing time if provided and status is '完了'
        if new_status == "完了" and processing_time_sec is not None:
            file_info.processing_time_str = f"({processing_time_sec:.1f}s)"
        elif new_status != "完了": # Clear time if status changes from completed
             file_info.processing_time_str = None

        # Update UI controls if they exist
        if file_info.status_text_control:
            file_info.status_text_control.value = new_status
            file_info.status_text_control.color = file_info.status_color
            # Disable dropdown if processing or completed? Optional.
            # if file_info.language_dropdown_control:
            #     file_info.language_dropdown_control.disabled = new_status in ["処理中", "完了", "エラー"]

        if file_info.time_text_control:
            file_info.time_text_control.value = file_info.processing_time_str or ""
            file_info.time_text_control.visible = bool(file_info.processing_time_str)

        # Request update for the specific Container (Row)
        if file_info.ui_control and list_view_control and list_view_control.page:
            file_info.ui_control.update() # Update the container which holds the row

def get_all_file_paths() -> List[str]:
    """Returns a list of all file paths currently managed."""
    return list(file_data.keys())

def get_file_info(file_path: str) -> Optional[FileInfo]:
     """Gets the FileInfo object for a given path."""
     return file_data.get(file_path)
