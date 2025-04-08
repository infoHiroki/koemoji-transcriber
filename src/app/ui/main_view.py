import flet as ft
from typing import TYPE_CHECKING, Callable, Optional

if TYPE_CHECKING:
    from flet import Control, Column, Row, Text, TextField, Ref, Container

def create_main_view(
    # Pass necessary controls and callbacks from main.py/handlers.py
    # file_list_container: 'Control', # Removed, left_panel_content is used instead
    plain_text_output_ref: 'Ref[TextField]',
    timestamped_output_ref: 'Ref[TextField]',
    copy_plain_text_callback: Callable,
    copy_timestamped_callback: Callable,
    left_panel_content: 'Control', # Add left_panel_content as an argument
) -> ft.Column: # Change return type hint
    """
    Creates the main view layout combining file list and result display.

    Args:
        left_panel_content: The control containing the file list and action buttons.
        plain_text_output_ref: Ref for the plain text output TextField.
        timestamped_output_ref: Ref for the timestamped text output TextField.
        copy_plain_text_callback: Callback function for copying plain text.
        copy_timestamped_callback: Callback function for copying timestamped text.

    Returns:
        A Row control representing the main view layout.
    """

    # --- Result Display Area (Right Side) ---
    plain_text_output = ft.TextField(
        ref=plain_text_output_ref,
        label="プレーンテキスト結果",
        multiline=True,
        read_only=True,
        expand=True,
        # min_lines=10, # Adjust height as needed
        border_color=ft.colors.OUTLINE,
    )

    timestamped_output = ft.TextField(
        ref=timestamped_output_ref,
        label="タイムスタンプ付き結果",
        multiline=True,
        read_only=True,
        expand=True,
        # min_lines=10, # Adjust height as needed
        border_color=ft.colors.OUTLINE,
    )

    copy_plain_button = ft.IconButton(
        icon=ft.icons.COPY,
        tooltip="プレーンテキストをコピー",
        on_click=copy_plain_text_callback,
    )
    copy_timestamped_button = ft.IconButton(
        icon=ft.icons.COPY,
        tooltip="タイムスタンプ付きテキストをコピー",
        on_click=copy_timestamped_callback,
    )

    # Remove guide text and its ref
    # guide_text_ref = ft.Ref[ft.Text]()
    # guide_text = ft.Text(...)

    result_column = ft.Column(
        [
            ft.Row([ft.Text("プレーンテキスト", weight=ft.FontWeight.BOLD), copy_plain_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            plain_text_output,
            ft.Divider(height=10, color=ft.colors.TRANSPARENT), # Spacer
            ft.Row([ft.Text("タイムスタンプ付き", weight=ft.FontWeight.BOLD), copy_timestamped_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            timestamped_output,
        ],
        expand=True,
        spacing=5,
        visible=True # Make result column always visible
    )

    result_container = ft.Container(
        content=result_column, # Directly use result_column, remove Stack
        expand=True,
    )


    # --- Main Layout (Top: File List, Bottom: Results) ---
    main_layout_column = ft.Column( # Change ft.Row to ft.Column
        [
            # Top Side (File List & Actions)
            ft.Container(
                content=left_panel_content,
                expand=1, # Change ratio to 1
            ),
            # Bottom Side (Results)
            ft.Container(
                content=result_container,
                expand=2, # Change ratio to 2
                padding=ft.padding.only(top=10), # Change padding from left to top
            ),
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.START, # Use MainAxisAlignment for vertical alignment in Column
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH # Stretch horizontally
    )

    return main_layout_column # Return the Column

# Helper function to toggle visibility (can be called from handlers)
def update_result_visibility(
    plain_text_ref: 'Ref[TextField]',
    timestamped_ref: 'Ref[TextField]',
    # guide_text_ref: 'Ref[Text]', # Removed guide text ref
    show_results: bool # Keep argument for now, but logic changes
):
    """Toggles the visibility of the result text fields vs guide text."""
    # This function might become obsolete or change significantly
    # For now, just ensure the result column is visible if show_results is True
    # The logic to clear/update fields is now handled directly in handle_file_selection
    if plain_text_ref.current and timestamped_ref.current:
        result_column = plain_text_ref.current.parent.parent
        if isinstance(result_column, ft.Column):
            if show_results and not result_column.visible:
                 result_column.visible = True
                 result_column.update()
            # No need to hide it anymore, just clear the fields in handle_file_selection
            # elif not show_results and result_column.visible:
            #      result_column.visible = False
            #      result_column.update()
            pass # Placeholder, actual update logic is in handle_file_selection
