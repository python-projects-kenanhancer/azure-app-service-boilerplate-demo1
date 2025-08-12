"""Performance monitoring middleware for detailed performance tracking."""

import time

import psutil

from ..decorators.pipeline_decorator import Context, Next
from ..logger.logger_strategies.logger_strategy import LoggerStrategy


def performance_middleware(context: Context, next: Next, logger: LoggerStrategy):
    """Middleware to track detailed performance metrics."""

    # Record start time and system metrics
    start_time = time.time()
    start_cpu = psutil.cpu_percent(interval=None)
    start_memory = psutil.virtual_memory().percent

    logger.info(f"[PERFORMANCE] Starting {context.func.__name__}")
    logger.info(f"[PERFORMANCE] Initial CPU: {start_cpu}%, Memory: {start_memory}%")

    try:
        # Process the request
        result = next()

        # Record end time and system metrics
        end_time = time.time()
        end_cpu = psutil.cpu_percent(interval=None)
        end_memory = psutil.virtual_memory().percent

        # Calculate metrics
        execution_time = end_time - start_time
        cpu_delta = end_cpu - start_cpu
        memory_delta = end_memory - start_memory

        # Log performance metrics
        logger.info(f"[PERFORMANCE] Completed {context.func.__name__}")
        logger.info(f"[PERFORMANCE] Execution time: {execution_time:.4f}s")
        logger.info(f"[PERFORMANCE] CPU change: {cpu_delta:+.2f}%")
        logger.info(f"[PERFORMANCE] Memory change: {memory_delta:+.2f}%")

        return result

    except Exception as e:
        # Log error with performance context
        end_time = time.time()
        execution_time = end_time - start_time
        logger.error(f"[PERFORMANCE] Error in {context.func.__name__} after {execution_time:.4f}s: {str(e)}")
        raise
