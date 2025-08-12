import json
import logging
import sys
import traceback
from datetime import datetime
from typing import Any, Dict, Optional

from .logger_strategy import LoggerStrategy


class DefaultLoggerStrategy(LoggerStrategy):
    def __init__(self, name: str = __name__):
        self._logger = logging.getLogger(name)
        self._logger_name = name

        # Only configure if no handlers are already set up
        if not self._logger.handlers:
            self._configure_logger()

    def _configure_logger(self):
        """Configure the logger with handlers and formatters optimized for Azure App Service"""
        # Set log level
        self._logger.setLevel(logging.INFO)

        # Create console handler (Azure App Service captures stdout)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        # Create formatter optimized for Azure
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        console_handler.setFormatter(formatter)

        # Add handler to logger
        self._logger.addHandler(console_handler)

        # Prevent propagation to avoid duplicate logs
        self._logger.propagate = False

    def _format_log_entry(self, level: str, message: str, **kwargs) -> str:
        """Format log entry with structured data for Azure"""
        log_entry: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level.upper(),
            "logger": self._logger_name,
            "message": message,
            "service": "azure_app_service",
            "environment": "production",  # This should come from settings
        }

        # Add any additional context
        if kwargs:
            log_entry["context"] = kwargs

        return json.dumps(log_entry)

    def _log_with_context(self, level: str, message: str, **kwargs) -> None:
        """Log with structured context for better Azure integration"""
        try:
            # For Azure App Service, structured JSON is better
            if kwargs:
                # Use structured logging when context is provided
                log_message = self._format_log_entry(level, message, **kwargs)
                getattr(self._logger, level.lower())(log_message)
            else:
                # Use simple format for basic messages
                getattr(self._logger, level.lower())(message)
        except Exception as e:
            # Fallback to basic logging if structured logging fails
            self._logger.error(f"Logging error: {str(e)} - Original message: {message}")

    def info(self, msg: str, *args, **kwargs) -> None:
        """Log info message with optional context"""
        if args:
            msg = msg % args
        self._log_with_context("info", msg, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        """Log warning message with optional context"""
        if args:
            msg = msg % args
        self._log_with_context("warning", msg, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        """Log error message with optional context and stack trace"""
        if args:
            msg = msg % args

        # Add stack trace for errors if not provided
        if "stack_trace" not in kwargs and "exc_info" not in kwargs:
            kwargs["stack_trace"] = traceback.format_exc()

        self._log_with_context("error", msg, **kwargs)

    def debug(self, msg, *args, **kwargs) -> None:
        """Log debug message with optional context"""
        if args:
            msg = msg % args
        self._log_with_context("debug", msg, **kwargs)

    def log_request(self, method: str, path: str, status_code: int, duration_ms: float, **kwargs) -> None:
        """Log HTTP request information for Azure monitoring"""
        self.info(
            f"HTTP {method} {path} - {status_code} - {duration_ms:.2f}ms",
            request_method=method,
            request_path=path,
            status_code=status_code,
            duration_ms=duration_ms,
            **kwargs,
        )

    def log_exception(self, exception: Exception, context: Optional[Dict[str, Any]] = None) -> None:
        """Log exception with full context for Azure error tracking"""
        error_context = {
            "exception_type": type(exception).__name__,
            "exception_message": str(exception),
            "stack_trace": traceback.format_exc(),
        }

        if context:
            error_context.update(context)

        self.error(f"Exception occurred: {str(exception)}", **error_context)
