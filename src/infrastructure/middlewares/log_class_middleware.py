from injector import inject

from ..decorators.pipeline_decorator import Context, Next
from ..logger.logger_strategies.logger_strategy import LoggerStrategy


class LogMiddleware:
    @inject
    def __init__(self, logger: LoggerStrategy):
        self.logger = logger

    def __call__(self, context: Context, next: Next):
        self.logger.info(f"[LOGGER] About to call {context.func.__name__}" f" with args={context.args}, kwargs={context.kwargs}")
        result = next()
        self.logger.info(f"[LOGGER] Finished {context.func.__name__}, result={result}")
        return result
