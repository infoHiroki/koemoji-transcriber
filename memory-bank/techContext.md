# Technical Context

## Core Technologies

*   **Programming Language:** Python
*   **GUI Framework:** [Flet](https://flet.dev/) (`flet==0.27.6`) - Used for building the desktop user interface.
*   **Transcription Engine:** [FasterWhisper](https://github.com/guillaumekln/faster-whisper) (`faster-whisper==1.1.1`) - Provides high-performance Whisper model inference.
    *   **Dependencies:**
        *   PyTorch (`torch==2.6.0`)
        *   CTranslate2 (`ctranslate2==4.5.0`)
    *   Installation details depend on the target environment (CPU/GPU). See `build_scripts/requirements.txt` and official documentation.

## Build & Distribution

*   **Bundling:** [PyInstaller](https://pyinstaller.org/) (Version not specified in requirements, likely installed globally or via other means) - Used to package the Python application into a standalone executable (`build_scripts/build_app.spec`).
*   **Installer:** [Inno Setup](https://jrsoftware.org/isinfo.php) (External tool, version not tracked in requirements) - Used to create the Windows installer (`build_scripts/create_installer.iss`).

## External Dependencies & Tools

*   **FFmpeg:** Required for audio processing (likely format conversion or manipulation before transcription). Binary seems to be included in `ffmpeg_bin/` (Version not tracked in requirements).
*   **Image Processing:** Pillow (`pillow==11.1.0`) - Used for icon conversion etc.
*   **Licensing (Optional):** May use WMI and pywin32 for generating/validating license keys based on hardware identifiers (commented out in `requirements.txt`).

## Development Setup Notes

*   Refer to `build_scripts/requirements.txt` for core Python dependencies.
*   Ensure correct PyTorch version (CPU or specific CUDA version) is installed based on the development/target machine.
*   FFmpeg needs to be accessible by the application, either via PATH or by referencing the included binary.
