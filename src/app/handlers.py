import flet as ft
import logging
import os
from typing import Optional, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from flet import (
        Page,
        FilePicker,
        FilePickerResultEvent,
        ControlEvent,
        Ref,
        TextField,
        Text,
        AlertDialog,
        SnackBar,
        Column, # Add Column for type hint
        Card # Add Card for type hint
    )
    # Import the new visibility toggle function
    from .ui.main_view import update_result_visibility
    from .ui.file_list_view import FileInfo, file_data, selected_file_path as selected_list_item_path, get_file_info
    # Remove old result view imports
    # from .ui.result_view import update_results as update_result_view, clear_results as clear_result_view, set_dropdown_value
    # Remove license imports (2025-04-07)
    # from .core.license import validate_license_key, save_license_key
    from .core.config import AppConfig

# --- State/Dependency Variables (to be passed in or set) ---
# These will be set by main.py after creating the handler instance or functions
page_ref: Optional['Page'] = None
file_picker_ref: Optional['FilePicker'] = None
app_config_ref: Optional['AppConfig'] = None
# Remove license refs (2025-04-07)
# license_dialog_ref: Optional['AlertDialog'] = None
# license_key_textfield_ref: Optional['Ref[TextField]'] = None
# license_error_text_ref: Optional['Ref[Text]'] = None
settings_output_folder_textfield_ref: Optional['Ref[TextField]'] = None
# Refs for the new main view result area (will be set in setup_handlers)
plain_text_output_ref: Optional['Ref[TextField]'] = None
timestamped_output_ref: Optional['Ref[TextField]'] = None
guide_text_ref: Optional['Ref[Text]'] = None # Ref for the guide text in main_view
file_list_card_ref: Optional['Ref[Card]'] = None # Ref for the file list card (recreated in main.py)
# Callbacks from other modules
add_files_to_list_callback: Optional[Callable] = None
update_result_visibility_callback: Optional[Callable] = None # New callback
# Remove old result view callbacks
# update_result_view_callback: Optional[Callable] = None
# clear_result_view_callback: Optional[Callable] = None
# set_dropdown_value_callback: Optional[Callable] = None
# Navigation content controls (passed from main)
main_view_content_ref: Optional[ft.Control] = None # New main view content
# file_processing_view_content_ref: Optional[ft.Control] = None # Removed
# result_view_content_ref: Optional[ft.Control] = None # Removed
settings_view_content_ref: Optional[ft.Control] = None
content_area_ref: Optional['Column'] = None # Explicitly type hint Column
file_data_ref: Optional[dict] = None # Add ref for file_data state


# --- Picker Action Context ---
_current_picker_action: Optional[str] = None

def set_picker_action(action: str):
    """Sets the current file picker action context."""
    global _current_picker_action
    _current_picker_action = action
    logging.info(f"Picker action set to: {action}")

# --- Picker Result Handlers (Internalized within combined handler) ---
def _handle_files_selected(e: 'FilePickerResultEvent'):
    """Internal handler for file selection results."""
    global page_ref, add_files_to_list_callback
    if not page_ref or not add_files_to_list_callback:
        logging.error("Handler dependencies not set for _handle_files_selected.")
        return
    logging.info("on_files_selected called.")
    if e.files:
        logging.info(f"Files received: {len(e.files)}")
        selected_files = [f.path for f in e.files if f.path]
        if selected_files:
            logging.info(f"Valid paths selected: {selected_files}")
            add_files_to_list_callback(selected_files) # Call the imported/passed function
            page_ref.snack_bar = ft.SnackBar(ft.Text(f"{len(selected_files)} 件のファイルを追加しました。"))
            page_ref.snack_bar.open = True
            logging.info("Files added to list and snackbar shown.")
        else:
            logging.warning("File selection event received, but no valid paths found.")
            page_ref.snack_bar = ft.SnackBar(ft.Text("有効なファイルが選択されませんでした。"))
            page_ref.snack_bar.open = True
    else:
        logging.info("File selection cancelled.")
        page_ref.snack_bar = ft.SnackBar(ft.Text("ファイル選択がキャンセルされました。"))
        page_ref.snack_bar.open = True
    if page_ref: page_ref.update() # Update page to show list changes and snackbar
    logging.info("_handle_files_selected finished.")

def _handle_default_output_dir_picked(e: 'FilePickerResultEvent'):
    """Internal handler for default output directory selection."""
    global page_ref, app_config_ref, settings_output_folder_textfield_ref
    if not page_ref or not app_config_ref or not settings_output_folder_textfield_ref:
        logging.error("Handler dependencies not set for _handle_default_output_dir_picked.")
        return
    logging.info("handle_default_output_dir_picked called.")
    target_textfield = settings_output_folder_textfield_ref.current
    if e.path:
        logging.info(f"Default Output Directory selected: {e.path}")
        if target_textfield:
            target_textfield.value = e.path
            try:
                app_config_ref.set('General', 'default_output_dir', e.path)
                app_config_ref.save_config()
                logging.info(f"Default output folder saved: {e.path}")
                page_ref.snack_bar = ft.SnackBar(ft.Text(f"出力先フォルダを {e.path} に設定しました。"), open=True)
            except Exception as ex:
                logging.error(f"Failed to save output folder setting: {ex}")
                page_ref.snack_bar = ft.SnackBar(ft.Text(f"出力先フォルダの設定保存に失敗しました: {ex}"), open=True)
            target_textfield.update()
        else:
            logging.warning("settings_output_folder_textfield_ref not found.")
    else:
        logging.info("Default Output Directory selection cancelled.")
        if page_ref: page_ref.update() # Update for snackbar if cancelled
    logging.info("handle_default_output_dir_picked finished.")

def _on_save_timestamp_file_picked(e: 'FilePickerResultEvent'):
    """Internal handler for saving timestamped text file."""
    global _current_picker_action, page_ref, selected_list_item_path, get_file_info
    if not page_ref or not get_file_info:
         logging.error("Handler dependencies not set for _on_save_timestamp_file_picked.")
         _current_picker_action = None # Reset action even on error
         return

    logging.info(f"on_save_timestamp_file_picked called. Action: {_current_picker_action}")
    if _current_picker_action != 'save_timestamp_file':
        logging.warning(f"on_save_timestamp_file_picked called with incorrect action: {_current_picker_action}")
        return # Don't reset action here, let the main handler do it

    save_path = e.path
    if save_path:
        logging.info(f"Timestamp save path selected: {save_path}")
        current_selected_path = selected_list_item_path # Get current selection from file_list_view state
        if not current_selected_path:
            logging.error("No file selected when save dialog returned.")
            page_ref.snack_bar = ft.SnackBar(ft.Text("エラー: 保存時にファイル選択が解除されました。"), open=True)
            page_ref.update()
            _current_picker_action = None
            return

        selected_info = get_file_info(current_selected_path)
        if not selected_info or not selected_info.timestamped_text:
            logging.error("No timestamped text found for selected file when saving.")
            page_ref.snack_bar = ft.SnackBar(ft.Text("エラー: 保存するタイムスタンプ付きテキストが見つかりません。"), open=True)
            page_ref.update()
            _current_picker_action = None
            return

        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(selected_info.timestamped_text)
            logging.info(f"Successfully saved timestamped text to: {save_path}")
            page_ref.snack_bar = ft.SnackBar(ft.Text(f"タイムスタンプ付きテキストを保存しました: {os.path.basename(save_path)}"), open=True)
        except Exception as ex:
            logging.error(f"Failed to save timestamped text to {save_path}: {ex}", exc_info=True)
            page_ref.snack_bar = ft.SnackBar(ft.Text(f"ファイルの保存中にエラーが発生しました: {ex}"), open=True)
        page_ref.update()
    else:
        logging.info("Timestamp save dialog cancelled.")
        page_ref.snack_bar = ft.SnackBar(ft.Text("タイムスタンプ付きテキストの保存がキャンセルされました。"), open=True)
        page_ref.update()

    _current_picker_action = None # Reset action after handling or cancellation

# --- Central File Picker Result Handler ---
def handle_picker_result_combined(e: 'FilePickerResultEvent'):
    """Handles results from all FilePicker actions."""
    global _current_picker_action
    action = _current_picker_action
    logging.info(f"handle_picker_result_combined called. Action: {action}")

    if action == 'pick_files':
        _handle_files_selected(e)
        _current_picker_action = None
    elif action == 'select_default_output':
        _handle_default_output_dir_picked(e)
        _current_picker_action = None
    elif action == 'save_timestamp_file':
        _on_save_timestamp_file_picked(e) # This handler resets the action internally
    else:
        logging.warning(f"Unhandled picker action in combined handler: {action}")
        _current_picker_action = None

    logging.info(f"Picker action after combined handler: {_current_picker_action}")

# --- Other UI Event Handlers ---

def handle_file_selection(selected_info: Optional['FileInfo']):
    """Callback when a file is selected in the list view. Updates the main result area."""
    global plain_text_output_ref, timestamped_output_ref # Removed guide_text_ref, update_result_visibility_callback
    if not plain_text_output_ref or not timestamped_output_ref: # Removed checks for removed refs/callbacks
        logging.error("Handler dependencies not set for handle_file_selection.")
        return

    plain_text_field = plain_text_output_ref.current
    timestamped_field = timestamped_output_ref.current

    if selected_info and plain_text_field and timestamped_field:
        logging.info(f"File selected: {selected_info.name}. Updating result view.")
        plain_text_field.value = selected_info.result_text or ""
        timestamped_field.value = selected_info.timestamped_text or ""
        # update_result_visibility_callback(plain_text_output_ref, timestamped_output_ref, guide_text_ref, True) # Removed visibility toggle
        plain_text_field.update()
        timestamped_field.update()
    else:
        logging.info("File selection cleared or refs not available. Clearing result view.")
        if plain_text_field:
            plain_text_field.value = ""
            plain_text_field.update()
        if timestamped_field:
            timestamped_field.value = ""
            timestamped_field.update()
        # update_result_visibility_callback(plain_text_output_ref, timestamped_output_ref, guide_text_ref, False) # Removed visibility toggle

# def handle_result_dropdown_change(e: 'ControlEvent'): # No longer needed
#     """Callback when the result dropdown selection changes."""
    #     pass # Replace entire body with pass to avoid syntax errors in commented code

def handle_copy_plain_text(e: 'ControlEvent'): # Add event argument 'e'
    """Copies the plain text result to the clipboard."""
    global page_ref, plain_text_output_ref # Use the correct ref name
    if not page_ref or not plain_text_output_ref: # Use the correct ref name
        logging.error("Handler dependencies not set for handle_copy_plain_text.")
        return
    text_output = plain_text_output_ref.current # Use the correct ref name
    if text_output and text_output.value:
        page_ref.set_clipboard(text_output.value)
        logging.info("Plain text copied to clipboard.")
        page_ref.snack_bar = ft.SnackBar(ft.Text("プレーンテキストをコピーしました。"), open=True)
    else:
        logging.info("No plain text to copy.")
        page_ref.snack_bar = ft.SnackBar(ft.Text("コピーするプレーンテキストがありません。"), open=True)
    page_ref.update()

def handle_copy_timestamped_text(e: 'ControlEvent'): # Add event argument 'e'
    """Copies the timestamped text result to the clipboard."""
    global page_ref, timestamped_output_ref # Use the correct ref name
    if not page_ref or not timestamped_output_ref: # Use the correct ref name
        logging.error("Handler dependencies not set for handle_copy_timestamped_text.")
        return
    timestamped_output = timestamped_output_ref.current # Use the correct ref name
    if timestamped_output and timestamped_output.value:
        page_ref.set_clipboard(timestamped_output.value)
        logging.info("Timestamped text copied to clipboard.")
        page_ref.snack_bar = ft.SnackBar(ft.Text("タイムスタンプ付きテキストをコピーしました。"), open=True)
    else:
        logging.info("No timestamped text to copy.")
        page_ref.snack_bar = ft.SnackBar(ft.Text("コピーするタイムスタンプ付きテキストがありません。"), open=True)
    page_ref.update()


# Removed handle_download_timestamps function (2025-04-05)

# Rename this function to handle clear button visibility
def update_clear_button_visibility(is_empty: bool):
    """Updates the visibility of the clear all button based on list content."""
    global clear_all_button_ref # Use the correct ref name
    if not clear_all_button_ref:
        logging.error("Handler dependencies not set for update_clear_button_visibility.")
        return

    target_button = clear_all_button_ref.current
    if target_button:
        should_be_visible = not is_empty
        if target_button.visible != should_be_visible:
            target_button.visible = should_be_visible
            if target_button.page:
                target_button.update()
            logging.info(f"Clear all button visibility updated to: {should_be_visible}")
    else:
        logging.warning("clear_all_button_ref not found during visibility update.")


def on_navigation_change(e: 'ControlEvent'):
    """Handles changes in the NavigationRail selection."""
    global content_area_ref, main_view_content_ref, settings_view_content_ref # Use new view refs
    if not content_area_ref or not main_view_content_ref or not settings_view_content_ref:
        logging.error("Handler dependencies not set for on_navigation_change.")
        return

    selected_index = e.control.selected_index
    logging.info(f"NavigationRail changed to index: {selected_index}")
    content_area = content_area_ref.current
    if not content_area:
         logging.error("Content area ref is not set.")
         return

    content_area.controls.clear()
    if selected_index == 0:
        content_area.controls.append(main_view_content_ref) # Show main view
    # elif selected_index == 1: # Removed result view index
    #     content_area.controls.append(result_view_content_ref)
    elif selected_index == 1: # Settings is now index 1
        content_area.controls.append(settings_view_content_ref)
    content_area.update()

# --- License Activation Handler Removed (2025-04-07) ---
# def activate_license(): ...

# --- Function to set dependencies ---
def setup_handlers(
    page: 'Page',
    file_picker: 'FilePicker',
    app_config: 'AppConfig',
    # license_dialog: 'AlertDialog', # Removed 2025-04-07
    refs: dict, # Pass a dictionary of refs
    callbacks: dict, # Pass a dictionary of callbacks
    views: dict, # Pass a dictionary of view content controls
    shared_state: dict # Add shared_state parameter
):
    """Sets up the necessary dependencies for the handler functions."""
    global page_ref, file_picker_ref, app_config_ref # Removed license_dialog_ref
    # Removed license refs (2025-04-07)
    # global license_key_textfield_ref, license_error_text_ref
    global settings_output_folder_textfield_ref
    # Update global refs
    global plain_text_output_ref, timestamped_output_ref, file_list_card_ref, file_data_ref, clear_all_button_ref # Add clear_all_button_ref
    global add_files_to_list_callback, update_result_visibility_callback, update_clear_button_visibility # Update callbacks
    global main_view_content_ref, settings_view_content_ref, content_area_ref # Update views
    # Removed license function imports (2025-04-07)
    # global validate_license_key, save_license_key
    global get_file_info, selected_list_item_path # Import necessary functions/state

    page_ref = page
    file_picker_ref = file_picker
    app_config_ref = app_config
    # license_dialog_ref = license_dialog # Removed 2025-04-07

    # Extract refs from the dictionary
    # license_key_textfield_ref = refs.get('license_key_textfield') # Removed 2025-04-07
    # license_error_text_ref = refs.get('license_error_text') # Removed 2025-04-07
    settings_output_folder_textfield_ref = refs.get('settings_output_folder_textfield')
    # Get new refs for main view
    plain_text_output_ref = refs.get('plain_text_output')
    timestamped_output_ref = refs.get('timestamped_output')
    # guide_text_ref = refs.get('guide_text') # Removed guide_text ref
    file_list_card_ref = refs.get('file_list_card')
    clear_all_button_ref = refs.get('clear_all_button') # Get clear button ref
    content_area_ref = refs.get('content_area')

    # Extract callbacks
    add_files_to_list_callback = callbacks.get('add_files_to_list')
    update_result_visibility_callback = callbacks.get('update_result_visibility') # Get new callback
    update_clear_button_visibility = callbacks.get('update_clear_button_visibility') # Get new callback
    # Remove old callbacks
    # update_result_view_callback = callbacks.get('update_result_view')
    # clear_result_view_callback = callbacks.get('clear_result_view')
    # set_dropdown_value_callback = callbacks.get('set_dropdown_value')
    # Import functions needed by handlers
    # validate_license_key = callbacks.get('validate_license_key') # Removed 2025-04-07
    # save_license_key = callbacks.get('save_license_key') # Removed 2025-04-07
    get_file_info = callbacks.get('get_file_info')
    selected_list_item_path = callbacks.get('selected_list_item_path') # This needs careful handling if it's state

    # Extract shared state
    file_data_ref = shared_state.get('file_data') # Assign passed file_data dict

    # Extract view content controls
    main_view_content_ref = views.get('main') # Get new main view
    # file_processing_view_content_ref = views.get('file_processing') # Removed
    # result_view_content_ref = views.get('result') # Removed
    settings_view_content_ref = views.get('settings')

    # Assign the central picker handler
    if file_picker_ref:
        file_picker_ref.on_result = handle_picker_result_combined

    logging.info("Handlers setup complete.")
