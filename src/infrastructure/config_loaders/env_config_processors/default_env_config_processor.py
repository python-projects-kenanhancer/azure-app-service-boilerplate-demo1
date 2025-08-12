import json
import logging
from typing import Any

from .env_config_processor import EnvConfigProcessor


class DefaultEnvConfigProcessor(EnvConfigProcessor):
    """
    Processes flat environment dictionaries into nested dictionaries with JSON fields parsed.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def process(self, flat_dict: dict[str, str | Any]) -> dict[str, Any]:
        """
        Process a flat dictionary into a nested dictionary with JSON fields parsed.
        :param flat_dict: Flat dictionary to process.
        :return: Fully processed nested dictionary.
        """
        try:
            nested_env = self._nest_dict(flat_dict)
            self._parse_json_fields(nested_env)
            self.logger.info("Successfully processed environment variables.")
            return nested_env
        except Exception as e:
            self.logger.error(f"Error processing environment variables: {e}")
            raise

    def _parse_json_fields(self, nested_env: dict[str, str | dict[str, Any]]) -> None:
        """
        Recursively parse JSON strings in a nested dictionary.

        :param nested_env: Nested dictionary to process.
        """
        for key, value in nested_env.items():
            if isinstance(value, dict):
                self._parse_json_fields(value)
            else:
                try:
                    nested_env[key] = json.loads(value)
                    self.logger.info(f"Parsed JSON field for key: {key}")
                except (json.JSONDecodeError, TypeError):
                    self.logger.debug(f"Skipping non-JSON field for key: {key}")

    def _nest_dict(self, flat_dict: dict[str, str | Any]) -> dict[str, Any]:
        """
        Transform a flat dictionary with double underscores into nested dictionaries.

        :param flat_dict: Flat dictionary to transform.
        :return: Nested dictionary.
        """
        nested: dict[str, Any] = {}
        for key, value in flat_dict.items():
            keys = key.lower().split("__")
            current_level = nested
            for part in keys[:-1]:
                if part not in current_level or not isinstance(current_level[part], dict):
                    current_level[part] = {}
                current_level = current_level[part]
            current_level[keys[-1]] = value
            self.logger.debug(f"Nesting key: {key}")
        self.logger.info("Successfully nested environment variables.")
        return nested
