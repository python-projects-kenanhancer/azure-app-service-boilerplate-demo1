import json
import logging
from typing import Any

from .config_loader import ConfigLoader
from .config_providers import ConfigProvider


class JsonConfigLoader(ConfigLoader):
    """
    Loads configuration from a JSON source provided by a ConfigProvider.
    """

    def __init__(self, config_provider: ConfigProvider):
        """
        Initialize the JSON loader with a configuration provider.
        :param config_provider: Instance of ConfigProvider to fetch configuration content.
        """
        self.config_provider = config_provider
        self.logger = logging.getLogger(self.__class__.__name__)

    def load(self) -> dict[str, Any]:
        """
        Load and parse the JSON configuration.

        :return: Parsed configuration as a dictionary.
        :raises json.JSONDecodeError: If the JSON content is invalid.
        :raises ValueError: If the configuration content is empty.
        :raises Exception: For any unexpected errors.
        """
        try:
            config_content = self.config_provider.get_config()
            if config_content is None or not config_content.strip():
                raise ValueError("Configuration content is empty or invalid.")

            parsed_content = json.loads(config_content)  # Safely parse JSON content
            self.logger.info("Successfully parsed JSON configuration.")
            return parsed_content
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON content: {e}")
            raise
        except ValueError as e:
            self.logger.error(f"Error: {e}")
            raise
        except Exception as e:
            self.logger.exception(f"Unexpected error while loading JSON configuration: {e}")
            raise
