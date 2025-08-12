from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class LoggerStrategy(ABC):
    @abstractmethod
    def info(self, msg: str, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def warning(self, msg: str, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def error(self, msg: str, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def debug(self, msg, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def log_request(self, method: str, path: str, status_code: int, duration_ms: float, **kwargs) -> None:
        """Log HTTP request information for monitoring"""
        pass

    @abstractmethod
    def log_exception(self, exception: Exception, context: Optional[Dict[str, Any]] = None) -> None:
        """Log exception with full context for error tracking"""
        pass
