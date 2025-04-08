import flet as ft
import logging
from flet import (
    FilePicker,
    # FilePickerResultEvent, # No longer needed directly
    # FilePickerFileType, # No longer needed directly
    Page,
    Row,
    Column,
    Text,
    ElevatedButton,
    MainAxisAlignment,
    CrossAxisAlignment,
    ProgressRing,
    SnackBar, # Keep for error display during init
    TextButton, # Import TextButton
    Divider,
    VerticalDivider,
    icons, # Keep for NavigationRailDestination
    colors, # Keep for error display during init
    AlertDialog,
    NavigationRail,
    NavigationRailDestination,
    TextField,
    # Checkbox, # No longer needed directly
    # IconButton, # No longer needed directly
    # Dropdown, # No longer needed directly
    # dropdown, # No longer needed directly
    Ref,
    Container, # Keep for layout
    padding, # Keep for layout
    alignment, # Keep for layout
    Card # Keep for type hints
)
# Import UI creation functions
from app.ui.file_list_view import (
    create_file_list_view,
    add_files as add_files_to_list, # Keep for handlers setup
    get_all_file_paths as get_list_file_paths, # Keep for processing setup
    get_file_info, # Keep for handlers/processing setup
    update_file_status, # Keep for processing setup
    FileInfo, # Keep for type hints
    selected_file_path as selected_list_item_path, # Keep for processing setup
    file_data, # Keep for processing setup
    clear_all_files # Import the clear_all_files function
)
# Remove import from deleted result_view module
# from app.ui.result_view import (
#     create_result_view,
#     update_results as update_result_view_callback, # Rename for clarity
#     clear_results as clear_result_view_callback, # Rename for clarity
#     update_dropdown_options, # Keep for processing setup
#     set_dropdown_value, # Keep for handlers setup
#     text_output_control_ref as result_text_output_ref, # Import Ref from result_view
#     timestamped_output_control_ref as result_timestamped_output_ref, # Import Ref from result_view
#     # filename_display_ref, # Removed as it's no longer defined in result_view
#     result_selector_dropdown_ref # Import Ref from result_view
# )
from app.ui.settings_tab import create_settings_tab
# from app.ui.file_processing_tab import create_file_processing_tab # Removed
from app.ui.main_view import create_main_view, update_result_visibility # Import new view
# Import Core Services
from app.core.transcription import TranscriptionService
from app.core.config import AppConfig
# Remove license imports (2025-04-07)
# from app.core.license import (
#     check_license,
#     validate_license_key,
#     save_license_key,
#     get_hardware_fingerprint,
# )
# Import New Modules
from app.handlers import (
    setup_handlers, set_picker_action, handle_file_selection,
    # handle_result_dropdown_change, # Removed as the function is commented out in handlers.py
    handle_copy_plain_text, handle_copy_timestamped_text, # Import new copy handlers
    # handle_download_timestamps, # Removed download handler import
    update_clear_button_visibility, on_navigation_change, # Removed activate_license import
    # Import the helper function reference needed by handlers
    # guide_text_ref # This ref is created in main_view, need to pass it differently or access via main_view controls
)
from app.core.processing import setup_processing, start_processing
# Import Helpers
from utils.helpers import generate_output_filename # Keep for processing setup
# Standard Imports
import os
import sys
import threading # Import threading for background initialization
import time
import traceback
from typing import Optional, Callable, Any # Keep for type hints, Add Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Main UI Building Function ---
def build_main_ui(
    page: Page,
    app_config: AppConfig,
    transcription_service: TranscriptionService
    # Removed license_dialog parameter (2025-04-07)
) -> ft.Row:
    """Builds the main UI layout Row."""
    logging.info("Building main UI...")
    # --- UI Components Refs ---
    progress_ring_ref = ft.Ref[ProgressRing]()
    start_button_ref = ft.Ref[ElevatedButton]()
    # license_key_textfield_ref = ft.Ref[TextField]() # Removed 2025-04-07
    # license_error_text_ref = ft.Ref[Text]() # Removed 2025-04-07
    content_area_ref = ft.Ref[Column]()
    add_files_button_ref = ft.Ref[ElevatedButton]()
    clear_all_button_ref = ft.Ref[TextButton]()
    cancel_button_ref = ft.Ref[ElevatedButton]()
    settings_output_folder_textfield_ref: Optional[ft.Ref[TextField]] = None
    plain_text_output_ref = ft.Ref[TextField]()
    timestamped_output_ref = ft.Ref[TextField]()
    guide_text_ref = ft.Ref[Text]() # Ref for the guide text in main_view (created inside main_view)
    file_list_card_ref = ft.Ref[ft.Card]()

    # --- File Picker Setup ---
    file_picker = FilePicker()

    # --- Create UI View Content Controls ---
    file_list_view_control = create_file_list_view(
        select_callback=handle_file_selection,
        list_change_callback=update_clear_button_visibility
    )
    add_files_button = ft.ElevatedButton(
        ref=add_files_button_ref,
        text="音声ファイルを追加",
        icon=ft.Icons.ADD, # Use ft.Icons
        tooltip="処理する音声ファイルを選択してリストに追加します",
        on_click=lambda _: (
            set_picker_action('pick_files'),
            file_picker.pick_files(
                allow_multiple=True,
                allowed_extensions=["mp3", "wav", "m4a", "flac", "ogg", "aac", "wma"],
                dialog_title="音声ファイルを選択"
            )
        )
    )
    start_button_control = ft.ElevatedButton(
        ref=start_button_ref,
        text="処理開始",
        icon=ft.Icons.PLAY_ARROW_ROUNDED, # Use ft.Icons (alternative)
        tooltip="リスト内のファイルの文字起こしを開始します",
        on_click=lambda _: start_processing(),
        disabled=False
    )
    progress_ring_control = ft.ProgressRing(
        ref=progress_ring_ref,
        visible=False,
        width=16,
        height=16,
        stroke_width=2
    )
    action_row = ft.Row([add_files_button, start_button_control, progress_ring_control])
    clear_all_button = ft.TextButton(
        ref=clear_all_button_ref,
        text="全てクリア",
        icon=ft.Icons.DELETE_SWEEP_OUTLINED, # Use ft.Icons (alternative)
        tooltip="リスト内の全てのファイルを削除します",
        on_click=lambda _: clear_all_files(),
        visible=False,
    )
    clear_all_button_row = ft.Row(
        [clear_all_button],
        alignment=ft.MainAxisAlignment.END
    )
    file_list_card = ft.Card(
        ref=file_list_card_ref,
        content=file_list_view_control,
        expand=True,
    )
    left_panel_content = ft.Column(
        [
            action_row,
            file_list_card,
            clear_all_button_row,
        ],
        spacing=10,
        expand=True,
    )
    main_view_content = create_main_view(
        left_panel_content=left_panel_content,
        plain_text_output_ref=plain_text_output_ref,
        timestamped_output_ref=timestamped_output_ref,
        copy_plain_text_callback=handle_copy_plain_text,
        copy_timestamped_callback=handle_copy_timestamped_text,
    )
    detected_device_str = transcription_service.device.upper()
    settings_view_content, returned_settings_ref = create_settings_tab(
         page, app_config, file_picker, set_picker_action,
         detected_device_str=detected_device_str
    )
    settings_output_folder_textfield_ref = returned_settings_ref

    # --- Setup Handlers and Processing Modules ---
    handler_refs = {
        # 'license_key_textfield': license_key_textfield_ref, # Removed 2025-04-07
        # 'license_error_text': license_error_text_ref, # Removed 2025-04-07
        'settings_output_folder_textfield': settings_output_folder_textfield_ref,
        'plain_text_output': plain_text_output_ref,
        'timestamped_output': timestamped_output_ref,
        'file_list_card': file_list_card_ref,
        'clear_all_button': clear_all_button_ref,
        'content_area': content_area_ref # Pass ref from main scope
    }
    handler_callbacks = {
        'add_files_to_list': add_files_to_list,
        'update_result_visibility': update_result_visibility,
        'update_clear_button_visibility': update_clear_button_visibility,
        # 'validate_license_key': validate_license_key, # Removed 2025-04-07
        # 'save_license_key': save_license_key, # Removed 2025-04-07
        'get_file_info': get_file_info,
        'selected_list_item_path': selected_list_item_path,
        # Removed build_main_ui callback as it's no longer needed by handlers
        # 'build_main_ui': lambda: build_main_ui(page, app_config, transcription_service)
    }
    handler_views = {
        'main': main_view_content,
        'settings': settings_view_content
    }
    # Note: setup_handlers no longer needs license_dialog
    setup_handlers(
        page=page,
        file_picker=file_picker,
        app_config=app_config,
        # license_dialog=license_dialog, # Removed 2025-04-07
        refs=handler_refs,
        callbacks=handler_callbacks,
        views=handler_views,
        shared_state={'file_data': file_data}
    )
    processing_refs = {
        'progress_ring': progress_ring_ref,
        'start_button': start_button_ref
    }
    processing_callbacks = {
        'get_list_file_paths': get_list_file_paths,
        'get_file_info': get_file_info,
        'update_file_status': update_file_status,
        'handle_file_selection': handle_file_selection,
        'generate_output_filename': generate_output_filename
    }
    processing_shared_state = {
        'selected_list_item_path': selected_list_item_path,
        'file_data': file_data
    }
    setup_processing(
        page=page,
        transcription_service=transcription_service,
        app_config=app_config,
        refs=processing_refs,
        callbacks=processing_callbacks,
        shared_state=processing_shared_state
    )

    # --- Navigation Rail and Content Area ---
    content_area_control = ft.Column(
        ref=content_area_ref, # Use ref from main scope
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH
    )
    navigation_rail = NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        group_alignment=-0.9,
        destinations=[
            NavigationRailDestination(
                icon=ft.Icons.UPLOAD_FILE_OUTLINED,
                selected_icon=ft.Icons.UPLOAD_FILE,
                label="メイン"
            ),
            NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
                label="設定",
            ),
        ],
        on_change=on_navigation_change,
    )

    # Add the main view content initially to the content area
    content_area_control.controls.append(main_view_content)

    main_layout_row = Row(
        [
            navigation_rail,
            VerticalDivider(width=1),
            content_area_control,
        ],
        expand=True,
        vertical_alignment=CrossAxisAlignment.START
    )

    # Add FilePicker to overlay (needs to be done once per page)
    if file_picker not in page.overlay:
        page.overlay.append(file_picker)

    logging.info("Main UI built.")
    return main_layout_row


# --- Background Initialization Function ---
def initialize_app_background(page: Page, loading_container: ft.Container):
    """Handles heavy initialization in a background thread."""
    try:
        logging.info("Background initialization started...")
        # --- Core Services ---
        app_config = AppConfig()
        # Update loading text
        if loading_container.content and isinstance(loading_container.content, ft.Column):
             loading_text = loading_container.content.controls[1]
             if isinstance(loading_text, ft.Text):
                  loading_text.value = "モデルを読み込んでいます..."
                  page.run_thread_safe(loading_container.update)

        transcription_service = TranscriptionService(config=app_config) # This loads the model

        # Check if model loading failed (assuming TranscriptionService sets self.model to None on failure)
        if transcription_service.model is None:
             raise RuntimeError("Failed to load the transcription model.")

        # --- Build Main UI ---
        main_layout = build_main_ui(page, app_config, transcription_service) # Build the main UI

        # --- Switch UI in Main Thread ---
        def update_ui_main_thread():
            logging.info("Switching to main UI...")
            page.controls.clear() # Clear loading screen
            page.add(main_layout)
            page.update()
            logging.info("Main UI displayed.")

        page.run_thread_safe(update_ui_main_thread)

    except Exception as e:
        logging.error(f"Error during background initialization: {e}", exc_info=True)
        # --- Show Error in Main Thread ---
        def show_error_main_thread():
            page.controls.clear() # Clear loading screen
            page.add(ft.Text(f"初期化中にエラーが発生しました: {e}", color=ft.colors.RED, size=16))
            page.update()
        page.run_thread_safe(show_error_main_thread)


def main(page: Page):
    """
    Main function for the Flet application.
    Initializes the UI and sets page properties.
    """
    try: # Start try block for initialization
        page.title = "Koemoji - 文字起こしツール"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.vertical_alignment = MainAxisAlignment.START
        page.horizontal_alignment = CrossAxisAlignment.STRETCH
        page.window_width = 1000
        page.window_height = 700 # Fix indentation
        page.window_resizable = True # Fix indentation
        page.window_icon = "src/assets/koemoji-infinity-logo-256x256.ico"

        logging.info("Application started.")

        # --- Loading Screen ---
        loading_indicator = ft.ProgressRing()
        loading_text = ft.Text("アプリケーションを初期化中...", size=16)
        loading_container = ft.Container(
            content=ft.Column(
                [loading_indicator, loading_text],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ),
            alignment=ft.alignment.center,
            expand=True
        )

        # --- Display Loading Screen Immediately ---
        page.add(loading_container)
        page.update()

        # --- Start Background Initialization ---
        init_thread = threading.Thread(
            target=initialize_app_background,
            args=(page, loading_container), # Pass page and loading container
            daemon=True
        )
        init_thread.start()

        # --- The rest of the UI building and setup is now done in initialize_app_background ---
        # --- We remove the direct calls from here ---

        # --- Core Services Removed (moved to background) ---
        # app_config = AppConfig()
        # transcription_service = TranscriptionService(config=app_config)

        # --- UI Components Refs Removed (moved to build_main_ui) ---
        # progress_ring_ref = ft.Ref[ProgressRing]()
        # start_button_ref = ft.Ref[ElevatedButton]()
        # content_area_ref = ft.Ref[Column]()
        # add_files_button_ref = ft.Ref[ElevatedButton]()
        # clear_all_button_ref = ft.Ref[TextButton]()
        # cancel_button_ref = ft.Ref[ElevatedButton]()
        # settings_output_folder_textfield_ref: Optional[ft.Ref[TextField]] = None
        # plain_text_output_ref = ft.Ref[TextField]()
        # timestamped_output_ref = ft.Ref[TextField]()
        # guide_text_ref = ft.Ref[Text]()

        # --- File Picker Setup Removed (moved to build_main_ui) ---
        # file_picker = FilePicker()

        # --- License Activation Dialog Removed (2025-04-07) ---

        # --- Create UI View Content Controls Removed (moved to build_main_ui) ---
        # file_list_view_control = create_file_list_view(...)
        # add_files_button = ft.ElevatedButton(...)
        # start_button_control = ft.ElevatedButton(...)
        # progress_ring_control = ft.ProgressRing(...)
        # action_row = ft.Row(...)
        # clear_all_button = ft.TextButton(...)
        # clear_all_button_row = ft.Row(...)
        # file_list_card_ref = ft.Ref[ft.Card]()
        # file_list_card = ft.Card(...)
        # left_panel_content = ft.Column(...)
        # main_view_content = create_main_view(...)
        # Settings View Removed (moved to build_main_ui)
        # settings_view_content, returned_settings_ref = create_settings_tab(...)
        # settings_output_folder_textfield_ref = returned_settings_ref

        # --- Setup Handlers and Processing Modules Removed (moved to build_main_ui) ---
        # handler_refs = {...}
        # handler_callbacks = {...}
        # handler_views = {...}
        # setup_handlers(...)
        # processing_refs = {...}
        # processing_callbacks = {...}
        # processing_shared_state = {...}
        # setup_processing(...)
        # --- Navigation Rail and Content Area Removed (moved to build_main_ui) ---
        # content_area_control = ft.Column(...)
        # navigation_rail = NavigationRail(...)
        # --- Main Layout Construction Removed (moved to build_main_ui) ---
        # main_layout_row = Row(...)
        # --- Initial Page Setup Removed (handled by loading screen logic) ---
        # page.add(main_layout_row)
        # page.overlay.append(file_picker)
        # page.update()

        # --- License Dialog Logic Removed ---

        # logging.info("Initial page update complete.") # Logging moved

    except Exception as e: # Keep top-level exception handling for initial setup
        logging.error(f"An error occurred during application initialization: {e}", exc_info=True) # Ensure except is aligned with try
        try: # Ensure content of except is indented
            page.clean()
            page.add(ft.Text(f"アプリケーションの起動中にエラーが発生しました: {e}\n詳細はログを確認してください。", color=ft.colors.RED, size=14))
            page.update()
        except Exception as page_err: # Ensure content of except is indented
            logging.error(f"Failed to display error on page: {page_err}")


if __name__ == "__main__":
    ft.app(target=main)
