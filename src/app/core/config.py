import configparser
import os
import logging

class AppConfig:
    def __init__(self, config_file="settings.ini"):
        # Define path relative to user's AppData or similar appropriate location
        # For simplicity here, using current dir, but change for production
        app_data_dir = os.getenv('APPDATA') or os.path.expanduser("~")
        config_dir = os.path.join(app_data_dir, "WhisperDesktopTranscriber") # Example name
        if not os.path.exists(config_dir):
            try:
                os.makedirs(config_dir)
            except OSError as e:
                logging.error(f"Failed to create config directory {config_dir}: {e}")
                # Fallback to current directory if AppData fails
                config_dir = "."

        self.config_path = os.path.join(config_dir, config_file)
        self.config = configparser.ConfigParser()
        self._load_defaults()
        self.load_config()
        logging.info(f"Config loaded from: {self.config_path}")

    def _load_defaults(self):
        """Sets default configuration values."""
        self.defaults = {
            'General': {
                'default_language': 'ja',
                'default_output_folder': os.path.expanduser("~/Documents"), # Example default
             },
             'Model': {
                 'model_path': 'base', # Default to 'base' model for faster testing
                 'device': 'auto' # auto, cpu, cuda
             }
            # 'Output' section removed 2025-04-07 as TXT saving is always enabled
            # Add license section later if needed
        }
        # Apply defaults to the config object initially
        for section, options in self.defaults.items():
            if not self.config.has_section(section):
                self.config.add_section(section)
            for key, value in options.items():
                if not self.config.has_option(section, key):
                    self.config.set(section, key, value)

    def load_config(self):
        """Loads configuration from the INI file."""
        try:
            if os.path.exists(self.config_path):
                self.config.read(self.config_path, encoding='utf-8')
                # Ensure all default sections/options exist after reading
                self._ensure_defaults_exist()
            else:
                logging.warning(f"Config file not found at {self.config_path}. Using defaults and creating.")
                self.save_config() # Create file with defaults if it doesn't exist
        except configparser.Error as e:
            logging.error(f"Error reading config file {self.config_path}: {e}")
            # Fallback to defaults if read fails
            self.config = configparser.ConfigParser()
            self._load_defaults()


    def _ensure_defaults_exist(self):
        """Ensures all default sections and options exist in the loaded config."""
        for section, options in self.defaults.items():
            if not self.config.has_section(section):
                self.config.add_section(section)
                logging.info(f"Added missing section [{section}] to config.")
            for key, value in options.items():
                if not self.config.has_option(section, key):
                    self.config.set(section, key, value)
                    logging.info(f"Added missing option '{key}' to section [{section}] with default value.")


    def save_config(self):
        """Saves the current configuration to the INI file."""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as configfile:
                self.config.write(configfile)
            logging.info(f"Configuration saved to {self.config_path}")
        except IOError as e:
            logging.error(f"Error writing config file {self.config_path}: {e}")
        except configparser.Error as e:
             logging.error(f"Error preparing config for saving: {e}")


    def get(self, section, key, fallback=None):
        """Gets a configuration value."""
        # Use defaults as fallback if not found in config object
        default_value = self.defaults.get(section, {}).get(key, fallback)
        return self.config.get(section, key, fallback=default_value)

    def getboolean(self, section, key, fallback=False):
        """Gets a boolean configuration value."""
        default_value = self.defaults.get(section, {}).get(key)
        # Convert default string 'True'/'False' to boolean if necessary
        if isinstance(default_value, str):
            default_value = default_value.lower() in ('true', '1', 't', 'y', 'yes')
        else: # Use provided fallback if default is not defined
             default_value = fallback

        try:
             return self.config.getboolean(section, key, fallback=default_value)
        except ValueError:
             logging.warning(f"Invalid boolean value for {section}.{key}. Falling back to {default_value}.")
             return default_value


    def set(self, section, key, value):
        """Sets a configuration value."""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value)) # Ensure value is string

# Example usage (optional, for testing)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    config = AppConfig()
    print(f"Default Language: {config.get('General', 'default_language')}")
    print(f"Save SRT: {config.getboolean('Output', 'save_srt')}")
    config.set('General', 'default_language', 'en')
    config.save_config()
    print(f"New Default Language: {config.get('General', 'default_language')}")
