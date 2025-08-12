import logging
from typing import Callable, Optional

from .greeting_strategies import BasicGreetingStrategy, GreetingStrategy
from .models import GreetingType


class GreetingStrategyFactory:
    """
    A factory that returns a GreetingStrategy based on some input.
    It also maintains a registry of custom strategies, if needed.
    """

    _default_instance: Optional["GreetingStrategyFactory"] = None

    def __init__(self) -> None:
        self._greeting_registry: dict[GreetingType, Callable[[], GreetingStrategy]] = {}
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("GreetingStrategyFactory initialized with an empty registry.")

    @classmethod
    def default(cls) -> "GreetingStrategyFactory":
        """
        Returns a singleton-like default instance of the factory.
        """
        if cls._default_instance is None:
            cls._default_instance = cls()
        return cls._default_instance

    def register(self, greeting_type: GreetingType, constructor: Callable[[], GreetingStrategy]) -> None:
        """
        Register a constructor for a specific GreetingType.
        If the type is already registered, this will overwrite the old registration.
        """
        if greeting_type in self._greeting_registry:
            self.logger.warning(
                "Overwriting existing registration for greeting type: %s",
                greeting_type,
            )
        self._greeting_registry[greeting_type] = constructor
        self.logger.info("Registered constructor for greeting type: %s", greeting_type)

    def create_greeting_strategy(self, greeting_type: GreetingType) -> GreetingStrategy:
        """
        Uses the registry to create a GreetingStrategy. If not found in the registry,
        falls back to default logic (e.g., returning BasicGreetingStrategy).
        """
        if greeting_type in self._greeting_registry:
            self.logger.info("Creating strategy from registry for greeting type: %s", greeting_type)
            return self._greeting_registry[greeting_type]()

        # Fallback logic, if not in registry:
        self.logger.warning("No registered strategy found for greeting type '%s'. Using fallback.", greeting_type)
        # Replace the below with your actual fallback:
        return BasicGreetingStrategy()
