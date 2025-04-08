import logging
import os
import time

def format_timestamp(seconds: float) -> str:
    """Formats seconds into HH:MM:SS.ms format."""
    milliseconds = int((seconds - int(seconds)) * 1000)
    return time.strftime('%H:%M:%S', time.gmtime(seconds)) + f'.{milliseconds:03d}'

def generate_output_filename(original_path: str, output_folder: str, extension: str) -> str:
    """Generates an output filename based on the original path and desired extension."""
    base_name = os.path.splitext(os.path.basename(original_path))[0]
    output_name = f"{base_name}.{extension}"
    return os.path.join(output_folder, output_name)

# Add more helper functions as needed, e.g., for file validation, etc.

if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    ts = format_timestamp(123.456)
    logging.info(f"Formatted timestamp: {ts}") # Expected: 00:02:03.456

    out_path = generate_output_filename("/path/to/my_audio.wav", "/output/dir", "txt")
    logging.info(f"Generated output path: {out_path}") # Expected: /output/dir/my_audio.txt (or \ on Windows)
