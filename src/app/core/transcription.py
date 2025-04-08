import logging
import time
import torch
from faster_whisper import WhisperModel
from .config import AppConfig # Import AppConfig to get settings
from utils.helpers import format_timestamp # Import helper for formatting
import os
import sys # Add this import

class TranscriptionService:
    def __init__(self, config: AppConfig):
        self.config = config
        self.model: WhisperModel | None = None
        self.device = self._detect_device()
        self.compute_type = "float16" if self.device == "cuda" else "int8" # Example compute type selection
        logging.info(f"TranscriptionService initialized. Detected device: {self.device}, Compute type: {self.compute_type}")
        self._load_model() # Load model on initialization

    def _detect_device(self):
        """Detects the appropriate device (CPU or CUDA), safely checking for CUDA availability."""
        config_device = self.config.get('Model', 'device', fallback='auto').lower()
        # Safely check if CUDA is available and supported by the installed PyTorch version
        cuda_available = hasattr(torch, 'cuda') and torch.cuda.is_available()

        if config_device == "cuda":
            if cuda_available:
                logging.info("CUDA device selected based on config and availability.")
                return "cuda"
            else:
                logging.warning("CUDA specified in config, but not available/supported. Falling back to CPU.")
                return "cpu"
        elif config_device == "auto":
            if cuda_available:
                logging.info("CUDA device selected automatically.")
                return "cuda"
            else:
                logging.info("CPU device selected automatically (CUDA not available).")
                return "cpu"
        else:
            logging.info("CPU device selected (config specified CPU or CUDA unavailable).")
            return "cpu"


    def _load_model(self):
        """Loads the FasterWhisper model based on config, prioritizing bundled model if available."""

        # Determine the base path for bundled resources
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Running in a PyInstaller bundle
            bundle_dir = sys._MEIPASS
            bundled_model_path = os.path.join(bundle_dir, 'models', 'large-v3') # Path inside the bundle
            logging.info(f"Running in bundled mode. Checking for bundled model at: {bundled_model_path}")
            if os.path.isdir(bundled_model_path):
                model_path = bundled_model_path # Use bundled model path
                logging.info(f"Using bundled model: {model_path}")
            else:
                logging.error(f"Bundled model directory not found at {bundled_model_path}. Cannot load model.")
                # Fallback or error handling needed? For now, let it proceed and likely fail later.
                model_path = self.config.get('Model', 'model_path', fallback='large-v3') # Fallback to config/default (will likely fail)
        else:
            # Not running in a bundle (development mode)
            logging.info("Running in development mode. Using model path from config or default.")
            model_path = self.config.get('Model', 'model_path', fallback='large-v3') # Use model name/path from config

        # --- The rest of the original _load_model method follows ---
        # Check if the path exists (only relevant for dev mode now)
        if not getattr(sys, 'frozen', False) and not os.path.isdir(model_path) and not os.path.isfile(model_path):
             logging.warning(f"Model path '{model_path}' not found locally (dev mode). Assuming it's a model name for download.")
             # FasterWhisper handles download if it's a valid model identifier like "large-v3"

        if self.model is None: # Avoid reloading if already loaded
            logging.info(f"Loading model '{model_path}' onto device '{self.device}' with compute type '{self.compute_type}'...")
            try:
                # Make sure model_path is defined before this point
                if 'model_path' not in locals() or model_path is None:
                     raise ValueError("Model path could not be determined.")
                self.model = WhisperModel(model_path, device=self.device, compute_type=self.compute_type)
                logging.info(f"Model '{model_path}' loaded successfully.")
            except Exception as e:
                logging.error(f"Failed to load model '{model_path}': {e}")
                self.model = None
        else:
             logging.info("Model already loaded.")


    def transcribe_audio(self, file_path: str, language: str | None = None): # Language can be None for auto-detect (if supported/enabled later)
        """
        Transcribes a single audio file using the loaded FasterWhisper model.
        This should run in a background thread.
        """
        if self.model is None:
            logging.error("Model is not loaded. Attempting to load again.")
            self._load_model() # Try loading again
            if self.model is None:
                 error_msg = "Model not available"
                 logging.error(error_msg)
                 return None, error_msg

        # Determine language: Use provided, fallback to config default, or None for auto-detect
        if language is None:
             language = self.config.get('General', 'default_language', fallback='ja')
             # Set language to None if you want FasterWhisper's auto-detection,
             # but requirements specify explicit language setting.
             # language = None # Uncomment for auto-detection

        logging.info(f"Starting transcription for: {file_path}, Language: {language}")
        start_time = time.time()

        try:
            # Actual transcription using FasterWhisper
            # TODO: Make beam_size, vad_filter etc. configurable if needed
            segments, info = self.model.transcribe(
                file_path,
                language=language,
                beam_size=5,
                vad_filter=True, # Enable VAD filter for potentially better accuracy/timing
                vad_parameters=dict(min_silence_duration_ms=500), # Example VAD param
            )

            result_text = ""
            timestamped_text = ""
            # Process segments generator
            for segment in segments:
                start_ts = format_timestamp(segment.start)
                end_ts = format_timestamp(segment.end)
                segment_text = segment.text.strip() # Remove leading/trailing whitespace
                result_text += segment_text + "\n" # Use single newline between segments
                timestamped_text += f"[{start_ts} --> {end_ts}] {segment_text}\n"

            detected_language = info.language
            lang_prob = info.language_probability
            duration = info.duration
            processing_time = time.time() - start_time

            logging.info(f"Detected language: {detected_language} (Prob: {lang_prob:.2f})")
            logging.info(f"Audio duration: {duration:.2f}s")
            logging.info(f"Transcription finished for {file_path} in {processing_time:.2f} seconds.")

            # Return tuple: ( (text_only, timestamped_text), error_message )
            return (result_text.strip(), timestamped_text.strip()), None

        except Exception as e:
            logging.exception(f"Transcription failed for {file_path}: {e}") # Use logging.exception to include traceback
            return None, f"Transcription error: {e}"
