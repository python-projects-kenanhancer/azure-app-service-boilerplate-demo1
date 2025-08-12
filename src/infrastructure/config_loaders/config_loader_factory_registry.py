import logging
from typing import Any, Callable, Dict, Optional, Type, TypeVar

from .config_loader import ConfigLoader
from .config_loader_args import ConfigLoaderArgs

T = TypeVar("T", bound="ConfigLoaderArgs")


class ConfigLoaderFactoryRegistry:
    """
    A hybrid factory class for creating configuration loaders.
    """

    _default_instance: Optional["ConfigLoaderFactoryRegistry"] = None

    def __init__(self):
        """
        Initialize a ConfigLoaderFactory with an empty registry.
        """
        self._loader_registry: Dict[Type[Any], Callable[[Any], ConfigLoader]] = {}
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("ConfigLoaderFactory initialized with an empty registry.")

    @classmethod
    def default(cls) -> "ConfigLoaderFactoryRegistry":
        """
        Retrieve the default factory instance, creating it if necessary.
        """
        if cls._default_instance is None:
            cls._default_instance = cls()
        return cls._default_instance

    def register(self, config_loader_args_type: Type[T], constructor: Callable[[T], ConfigLoader]) -> None:
        """
        Register a loader constructor for a specific argument type.

        :param config_loader_args_type: The type of arguments for the loader.
        :param constructor: A callable that accepts `config_loader_args` and returns a ConfigLoader instance.
        """
        if config_loader_args_type in self._loader_registry:
            self.logger.warning(f"Overwriting existing loader registration for: {config_loader_args_type}")
        self._loader_registry[config_loader_args_type] = constructor
        self.logger.info(f"Registered loader for config_loader_args type: {config_loader_args_type}")

    def get_loader(self, config_loader_args: ConfigLoaderArgs) -> ConfigLoader:
        """
        Create a loader based on the provided arguments.

        :param config_loader_args: Arguments specifying the loader type and details.
        :return: An instance of the appropriate loader.
        :raises ValueError: If no loader is registered for the argument type.
        """
        config_loader_args_type = type(config_loader_args)  # Dynamically determine the type of `config_loader_args`
        constructor = self._loader_registry.get(config_loader_args_type)

        if not constructor:
            self.logger.error(f"No loader registered for argument type: {config_loader_args_type}")
            raise ValueError(f"Unsupported loader arguments: {config_loader_args_type}")

        try:
            loader = constructor(config_loader_args)  # Pass `config_loader_args` to the constructor
            self.logger.info(f"Created loader: {loader.__class__.__name__} for config_loader_args: {config_loader_args}")
            return loader
        except Exception:
            self.logger.exception(f"Failed to create loader for config_loader_args: {config_loader_args}")
            raise
