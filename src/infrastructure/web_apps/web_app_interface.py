from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Tuple


class WebAppInterface(ABC):
    """Abstract interface for web applications"""

    @abstractmethod
    def add_route(self, path: str, methods: list[str], handler: Callable) -> None:
        """Add a route to the web application"""
        pass

    @abstractmethod
    def run(self, host: str = "0.0.0.0", port: int = 8000, debug: bool = False) -> None:
        """Run the web application"""
        pass

    @abstractmethod
    def create_response(self, data: Dict[str, Any], status_code: int = 200) -> Tuple[Any, int]:
        """Create a response object"""
        pass

    @abstractmethod
    def get_request_data(self) -> Dict[str, Any]:
        """Get data from the current request"""
        pass

    @abstractmethod
    def get_json_data(self, request) -> Dict[str, Any]:
        """Get JSON data from the request object (unified interface)"""
        pass
