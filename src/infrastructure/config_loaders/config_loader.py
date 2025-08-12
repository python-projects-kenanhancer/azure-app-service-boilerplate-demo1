from abc import ABC, abstractmethod
from typing import Any


class ConfigLoader(ABC):
    """
    Abstract base class for configuration loaders.
    All configuration loaders must implement the `load` method to provide
    configuration data as a dictionary.
    """

    @abstractmethod
    def load(self) -> dict[str, Any]:
        """
        Load configuration data and return it as a dictionary.

        :return: Configuration data as a dictionary.
        :raises Exception: Subclasses should raise exceptions for errors encountered while loading configuration.
        """
        pass
