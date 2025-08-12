import io
import logging
from typing import Any

from dotenv import dotenv_values

from .config_loader import ConfigLoader
from .config_providers.config_provider import ConfigProvider
from .env_config_processors import EnvConfigProcessor


class EnvConfigLoader(ConfigLoader):
    """
    Loads and processes environment variables provided by a ConfigProvider using an EnvConfigProcessor.
    """

    def __init__(self, config_provider: ConfigProvider, env_processor: EnvConfigProcessor):
        """
        Initialize the EnvLoader with a configuration provider and environment processor.
        :param config_provider: Instance of ConfigProvider to fetch environment configuration content.
        :param env_processor: Instance of EnvConfigProcessor to process environment variables.
        """
        self.config_provider = config_provider
        self.env_processor = env_processor
        self.logger = logging.getLogger(self.__class__.__name__)

    def load(self) -> dict[str, Any]:
        """
        Load and process environment variables.

        :return: Processed environment variables as a nested dictionary.
        :raises ValueError: If the environment payload is empty or invalid.
        :raises Exception: For any unexpected errors.
        """
        try:
            env_payload = self._fetch_env_payload()
            raw_env = self._parse_env_payload(env_payload)
            processed_env = self._process_env(raw_env)
            return processed_env
        except Exception as e:
            self.logger.exception(f"Unexpected error while loading environment variables: {e}")
            raise

    def _fetch_env_payload(self) -> str:
        """
        Fetch the environment configuration content from the provider.

        :return: Raw environment payload as a string.
        :raises ValueError: If the environment payload is empty or invalid.
        """
        try:
            payload = self.config_provider.get_config()
            if payload is None or not payload.strip():
                raise ValueError("Environment payload is empty or invalid.")
            self.logger.info("Successfully fetched environment payload.")
            return payload
        except Exception as e:
            self.logger.error(f"Error fetching environment payload: {e}")
            raise

    def _parse_env_payload(self, payload: str) -> dict[str, Any]:
        """
        Parse the raw environment payload into key-value pairs.

        :param payload: Raw environment payload as a string.
        :return: Parsed environment variables as a flat dictionary.
        """
        try:
            stream = io.StringIO(payload)  # Convert string to a stream
            env_vars = dotenv_values(stream=stream)
            self.logger.info("Successfully parsed environment payload.")
            return env_vars
        except Exception as e:
            self.logger.error(f"Error parsing environment payload: {e}")
            raise

    def _process_env(self, raw_env: dict[str, Any]) -> dict[str, Any]:
        """
        Process raw environment variables into a nested dictionary using the EnvConfigProcessor.

        :param raw_env: Flat dictionary of raw environment variables.
        :return: Nested dictionary of processed environment variables.
        """
        try:
            processed_env = self.env_processor.process(raw_env)
            self.logger.info("Successfully processed environment variables.")
            return processed_env
        except Exception as e:
            self.logger.error(f"Error processing environment variables: {e}")
            raise
