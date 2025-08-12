"""Request validation middleware for HTTP requests."""

from ..decorators.pipeline_decorator import Context, Next
from ..logger.logger_strategies.logger_strategy import LoggerStrategy


def request_validation_middleware(context: Context, next: Next, logger: LoggerStrategy):
    """Middleware to validate and log HTTP request details."""

    # Log request details
    logger.info(f"[REQUEST_VALIDATION] Processing {context.func.__name__}")

    # Extract request information if available
    if context.args and len(context.args) > 0:
        request = context.args[0]
        if hasattr(request, "method"):
            logger.info(f"[REQUEST_VALIDATION] HTTP Method: {request.method}")
        if hasattr(request, "url"):
            logger.info(f"[REQUEST_VALIDATION] URL: {request.url}")
        if hasattr(request, "headers"):
            logger.info(f"[REQUEST_VALIDATION] Headers: {dict(request.headers)}")

    # Process the request
    result = next()

    # Log response information
    logger.info(f"[REQUEST_VALIDATION] Completed {context.func.__name__}")

    return result
