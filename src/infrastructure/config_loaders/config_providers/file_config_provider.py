import logging

from .config_provider import ConfigProvider


class FileConfigProvider(ConfigProvider):
    """
    Provides configuration by reading the content of a YAML file.
    """

    def __init__(self, file_path: str):
        """
        Initialize the provider with the path to the YAML configuration file.
        :param file_path: Path to the YAML file.
        """
        self.file_path = file_path
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_config(self) -> str:
        """
        Reads the content of the YAML file.
        :return: File content as a string.
        :raises FileNotFoundError: If the file does not exist.
        :raises Exception: For any unexpected errors.
        """
        try:
            with open(self.file_path, "r") as file:
                return file.read()
        except FileNotFoundError as e:
            self.logger.error(f"Error: Configuration file not found at {self.file_path}: {e}")
            raise
        except Exception as e:
            self.logger.exception(f"Unexpected error while reading file {self.file_path}: {e}")
            raise
