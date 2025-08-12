from typing import Optional

from injector import Injector, Module

from ..config_loaders.config_loader_args import JsonConfigLoaderArgs
from .greeting_module import GreetingModule
from .logging_module import LoggingModule
from .redis_module import RedisModule
from .repositories_module import RepositoriesModule
from .settings_module import SettingsModule
from .sqlalchemy_module import SQLAlchemyModule
from .web_framework_module import WebFrameworkModule


def build_di_container(extra_modules: Optional[list[Module]] = None) -> Injector:
    base_modules = [
        SettingsModule(config_loader_args=JsonConfigLoaderArgs(file_path="config.json")),
        LoggingModule(),
        RedisModule(),
        SQLAlchemyModule(),
        RepositoriesModule(),
        GreetingModule(),
        WebFrameworkModule(),  # Add web framework module
    ]

    if extra_modules:
        base_modules.extend(extra_modules)

    return Injector(base_modules)
