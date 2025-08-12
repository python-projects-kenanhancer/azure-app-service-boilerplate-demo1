from typing import Type

from ..config_loader_args import EnvConfigLoaderArgs
from ..config_loader_factory import ConfigLoaderFactory
from .base_inject_settings import TSettings, inject_settings


def load_settings_from_env_file(*, file_path: str, SettingsClass: Type[TSettings]):
    env_config_loader = ConfigLoaderFactory.get_loader(EnvConfigLoaderArgs(file_path=file_path))

    raw_config = env_config_loader.load()
    return SettingsClass(**raw_config)


def inject_settings_from_env_file(file_path: str, param_name: str = "settings"):
    return inject_settings(load_settings_from_env_file, param_name=param_name, file_path=file_path)
