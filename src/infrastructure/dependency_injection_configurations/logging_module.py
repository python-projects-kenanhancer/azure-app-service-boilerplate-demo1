from injector import Module, provider, singleton

from ..logger import DefaultLoggerStrategy, LoggerStrategy
from ..models.settings import Settings


class LoggingModule(Module):
    @singleton
    @provider
    def provide_logger_strategy(self, settings: Settings) -> LoggerStrategy:
        return DefaultLoggerStrategy(settings.logger_name)
