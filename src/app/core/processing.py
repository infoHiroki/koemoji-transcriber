import flet as ft
import logging
import os
import threading
import time
from typing import Optional, Callable, List, TYPE_CHECKING

if TYPE_CHECKING:
    from flet import Page, Ref, ElevatedButton, ProgressRing, SnackBar
    from .transcription import TranscriptionService
    from .config import AppConfig
    from ..ui.file_list_view import FileInfo, file_data, get_file_info, update_file_status, get_all_file_paths, selected_file_path as selected_list_item_path
    # from ..ui.result_view import update_dropdown_options # Removed
    from ..utils.helpers import generate_output_filename
    from ..app.handlers import handle_file_selection # Import handler needed by thread

# --- State/Dependency Variables (to be passed in or set) ---
page_ref: Optional['Page'] = None
transcription_service_ref: Optional['TranscriptionService'] = None
app_config_ref: Optional['AppConfig'] = None
progress_ring_ref: Optional['Ref[ProgressRing]'] = None
start_button_ref: Optional['Ref[ElevatedButton]'] = None
# Callbacks/Functions from other modules
get_list_file_paths_callback: Optional[Callable[[], List[str]]] = None
get_file_info_callback: Optional[Callable[[str], Optional['FileInfo']]] = None
update_file_status_callback: Optional[Callable] = None
update_dropdown_options_callback: Optional[Callable[[List[ft.dropdown.Option]], None]] = None
handle_file_selection_callback: Optional[Callable[['FileInfo'], None]] = None # Callback from handlers
selected_list_item_path_ref: Optional[str] = None # State from file_list_view

# --- Background Processing Thread ---
def run_transcription_thread(files_to_process: list[str]):
    """Runs the transcription process in a background thread."""
    global page_ref, transcription_service_ref, app_config_ref, progress_ring_ref, start_button_ref
    global get_file_info_callback, update_file_status_callback # Removed update_dropdown_options_callback
    global handle_file_selection_callback, selected_list_item_path_ref, file_data

    if not all([page_ref, transcription_service_ref, app_config_ref, progress_ring_ref, start_button_ref,
                get_file_info_callback, update_file_status_callback, # Removed update_dropdown_options_callback
                handle_file_selection_callback]):
        logging.error("Processing dependencies not set.")
        # Attempt to reset UI state even on error
        if progress_ring_ref and progress_ring_ref.current: progress_ring_ref.current.visible = False
        if start_button_ref and start_button_ref.current: start_button_ref.current.disabled = False
        if page_ref: page_ref.update()
        return

    logging.info(f"Starting transcription thread for {len(files_to_process)} files.")
    completed_files_info: list[FileInfo] = []

    for file_path in files_to_process:
        file_info = get_file_info_callback(file_path)
        if not file_info:
            logging.warning(f"Could not get file info for {file_path}, skipping.")
            continue # Use continue inside a loop

        selected_language = file_info.language
        logging.info(f"Processing {file_info.name} with language: {selected_language}")

        update_file_status_callback(file_path, "処理中", ft.colors.ORANGE)

        start_time = time.time()
        logging.info(f"Starting transcription for {file_path} (Lang: {selected_language})...")
        results, error = transcription_service_ref.transcribe_audio(file_path, language=selected_language)
        end_time = time.time()
        processing_time = end_time - start_time

        if error:
            logging.error(f"Error during transcription for {file_path}: {error}")
            update_file_status_callback(file_path, f"エラー: {error[:30]}...", ft.colors.RED)
        else:
            logging.info(f"Transcription successful for {file_path} in {processing_time:.2f}s")
            file_info.result_text = results[0] if results else "No text result"
            file_info.timestamped_text = results[1] if results else "No timestamped result"
            update_file_status_callback(file_path, "完了", ft.colors.GREEN, processing_time_sec=processing_time)

            # --- Auto-save TXT result ---
            try:
                output_folder = app_config_ref.get('General', 'default_output_dir', fallback=".")
                if not output_folder:
                    output_folder = "."
                    logging.warning("Default output directory is empty in config, using current directory '.'")

                if not os.path.exists(output_folder):
                    logging.info(f"Creating output directory: {output_folder}")
                    os.makedirs(output_folder, exist_ok=True)

                # Correct indentation starts here
                txt_filename = generate_output_filename(file_path, output_folder, "txt")
                plain_text_result = results[0] if results and results[0] else ""
                timestamped_text_result = results[1] if results and results[1] else ""

                # Combine plain text and timestamped text with a separator
                combined_result = f"{plain_text_result}\n\n--- タイムスタンプ付きテキスト ---\n\n{timestamped_text_result}"

                # Save the combined result
                with open(txt_filename, 'w', encoding='utf-8') as f:
                    f.write(combined_result.strip()) # Use strip() to remove potential leading/trailing whitespace
                logging.info(f"Auto-saved combined result to: {txt_filename}")

            except Exception as save_ex: # Add except block here
                logging.error(f"Failed to auto-save combined result for {file_path} to '{output_folder}': {save_ex}", exc_info=True)
            # --- End Auto-save ---

            completed_files_info.append(file_info)

            # Update result view immediately after completion
            handle_file_selection_callback(file_info) # Call the handler to update result view

    # --- After all files are processed ---
    # Update dropdown options with completed files
    dropdown_opts = [
        ft.dropdown.Option(key=info.name, text=info.name)
        for info in completed_files_info if info.status == "完了"
    ]
    # Also include files that were already completed before this run
    for info in file_data.values(): # Access file_data directly (assuming it's shared state)
         if info not in completed_files_info and info.status == "完了":
              # This logic might be needed elsewhere if a dropdown is reintroduced
              # if not any(opt.key == info.name for opt in dropdown_opts):
              #      dropdown_opts.append(ft.dropdown.Option(key=info.name, text=info.name))
              pass # Keep loop structure for now, but do nothing with dropdown

    # Remove dropdown update logic
    # update_dropdown_options_callback(dropdown_opts)
    # logging.info(f"Result dropdown options updated with {len(dropdown_opts)} completed files.")

    # Update UI state (progress ring, buttons)
    if progress_ring_ref.current: progress_ring_ref.current.visible = False
    if start_button_ref.current: start_button_ref.current.disabled = False
    page_ref.snack_bar = ft.SnackBar(ft.Text("処理が完了しました。"))
    page_ref.snack_bar.open = True
    if page_ref: page_ref.update()

# --- Function to Start Processing ---
def start_processing():
    """Starts the transcription process in a new thread."""
    global page_ref, progress_ring_ref, start_button_ref, get_list_file_paths_callback
    if not all([page_ref, progress_ring_ref, start_button_ref, get_list_file_paths_callback]):
        logging.error("Processing start dependencies not set.")
        return

    logging.info("--- start_processing called ---")
    files_to_process = get_list_file_paths_callback()
    if not files_to_process:
        page_ref.snack_bar = ft.SnackBar(ft.Text("処理するファイルがありません。"))
        page_ref.snack_bar.open = True
        if page_ref: page_ref.update()
        return

    logging.info(f"Starting processing for {len(files_to_process)} files.")
    if progress_ring_ref.current: progress_ring_ref.current.visible = True
    if start_button_ref.current: start_button_ref.current.disabled = True
    page_ref.update()

    thread = threading.Thread(target=run_transcription_thread, args=(files_to_process,), daemon=True)
    thread.start()

# --- Function to set dependencies ---
def setup_processing(
    page: 'Page',
    transcription_service: 'TranscriptionService',
    app_config: 'AppConfig',
    refs: dict, # Pass refs: progress_ring, start_button
    callbacks: dict, # Pass callbacks: get_list_file_paths, get_file_info, update_file_status, handle_file_selection
    shared_state: dict # Pass shared state: selected_list_item_path, file_data
):
    """Sets up the necessary dependencies for the processing functions."""
    global page_ref, transcription_service_ref, app_config_ref
    global progress_ring_ref, start_button_ref
    global get_list_file_paths_callback, get_file_info_callback, update_file_status_callback
    # global update_dropdown_options_callback # Removed
    global handle_file_selection_callback
    global selected_list_item_path_ref, file_data, generate_output_filename # Import needed functions/state

    page_ref = page
    transcription_service_ref = transcription_service
    app_config_ref = app_config

    # Extract refs
    progress_ring_ref = refs.get('progress_ring')
    start_button_ref = refs.get('start_button')

    # Extract callbacks
    get_list_file_paths_callback = callbacks.get('get_list_file_paths')
    get_file_info_callback = callbacks.get('get_file_info')
    update_file_status_callback = callbacks.get('update_file_status')
    # update_dropdown_options_callback = callbacks.get('update_dropdown_options') # Removed
    handle_file_selection_callback = callbacks.get('handle_file_selection')
    generate_output_filename = callbacks.get('generate_output_filename') # Import helper

    # Extract shared state
    selected_list_item_path_ref = shared_state.get('selected_list_item_path')
    file_data = shared_state.get('file_data') # Get reference to the actual dict

    logging.info("Processing setup complete.")
