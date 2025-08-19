from injector import Module, provider

from ..config_loaders import ConfigLoaderArgs, load_settings_from_config_loader
from ..models.settings import Settings


class SettingsModule(Module):
    def __init__(self, config_loader_args: ConfigLoaderArgs):
        self.config_loader_args = config_loader_args

    @provider
    def provide_settings(self) -> Settings:
        settings = load_settings_from_config_loader(config_loader_args=self.config_loader_args, SettingsClass=Settings)
        return settings
