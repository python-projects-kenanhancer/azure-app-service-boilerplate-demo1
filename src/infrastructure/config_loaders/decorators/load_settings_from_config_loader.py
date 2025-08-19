from typing import Type

from ..config_loader_args import ConfigLoaderArgs
from ..config_loader_factory import ConfigLoaderFactory
from .base_inject_settings import TSettings


def load_settings_from_config_loader(*, config_loader_args: ConfigLoaderArgs, SettingsClass: Type[TSettings]):
    env_config_loader = ConfigLoaderFactory.get_loader(config_loader_args=config_loader_args)

    raw_config = env_config_loader.load()
    return SettingsClass(**raw_config)
