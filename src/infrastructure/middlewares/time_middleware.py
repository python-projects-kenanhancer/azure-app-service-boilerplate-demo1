import time

from ..decorators import Context, Next
from ..logger.logger_strategies.logger_strategy import LoggerStrategy


def time_middleware(context: Context, next: Next, logger: LoggerStrategy):
    start = time.time()
    logger.info("[TIME] Start timing...")
    result = next()
    elapsed = time.time() - start
    logger.info(f"[TIME] {context.func.__name__} took {elapsed:.4f}s")
    return result
