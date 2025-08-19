"""Error handling middleware for comprehensive error handling and logging."""

import traceback

from ..decorators.pipeline_decorator import Context, Next
from ..logger.logger_strategies.logger_strategy import LoggerStrategy


def error_handling_middleware(context: Context, next: Next, logger: LoggerStrategy):
    """Middleware to handle errors gracefully and provide detailed logging."""

    try:
        # Process the request
        result = next()
        return result

    except Exception as e:
        # Log detailed error information
        error_type = type(e).__name__
        error_message = str(e)
        function_name = context.func.__name__

        logger.error(f"[ERROR_HANDLING] Exception in {function_name}: {error_type}: {error_message}")
        logger.error(f"[ERROR_HANDLING] Function args: {context.args}")
        logger.error(f"[ERROR_HANDLING] Function kwargs: {context.kwargs}")
        logger.error(f"[ERROR_HANDLING] Stack trace: {traceback.format_exc()}")

        # You can customize error responses here based on the error type
        if isinstance(e, ValueError):
            # Return a user-friendly error response for validation errors
            return {"error": "Validation error", "message": error_message, "status": 400}
        elif isinstance(e, PermissionError):
            # Return a user-friendly error response for permission errors
            return {"error": "Permission denied", "message": error_message, "status": 403}
        else:
            # Return a generic error response for other errors
            return {"error": "Internal server error", "message": "An unexpected error occurred", "status": 500}
