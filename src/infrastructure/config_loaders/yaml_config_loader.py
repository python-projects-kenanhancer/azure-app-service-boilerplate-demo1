import logging
from typing import Any

import yaml

from .config_loader import ConfigLoader
from .config_providers import ConfigProvider


class YamlConfigLoader(ConfigLoader):
    """
    Loads configuration from a YAML source provided by a ConfigProvider.
    """

    def __init__(self, config_provider: ConfigProvider):
        """
        Initialize the YAML loader with a configuration provider.
        :param config_provider: Instance of ConfigProvider to fetch configuration content.
        """
        self.config_provider = config_provider
        self.logger = logging.getLogger(self.__class__.__name__)

    def load(self) -> dict[str, Any]:
        """
        Load and parse the YAML configuration.

        :return: Parsed configuration as a dictionary.
        :raises yaml.YAMLError: If the YAML content is invalid.
        :raises ValueError: If the configuration content is empty.
        :raises Exception: For any unexpected errors.
        """
        try:
            config_content = self.config_provider.get_config()
            if config_content is None or not config_content.strip():
                raise ValueError("Configuration content is empty or invalid.")

            parsed_content = yaml.safe_load(config_content)  # Safely parse YAML content
            self.logger.info("Successfully parsed YAML configuration.")
            return parsed_content
        except yaml.YAMLError as e:
            self.logger.error(f"Failed to parse YAML content: {e}")
            raise
        except ValueError as e:
            self.logger.error(f"Error: {e}")
            raise
        except Exception as e:
            self.logger.exception(f"Unexpected error while loading YAML configuration: {e}")
            raise
