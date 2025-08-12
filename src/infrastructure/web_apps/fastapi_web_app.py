from typing import Any, Callable, Dict

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .web_app_interface import WebAppInterface


class FastAPIWebApp(WebAppInterface):
    """FastAPI implementation of the WebAppInterface"""

    def __init__(self):
        self.app = FastAPI(title="Azure App Service API", version="1.0.0")

    def add_route(self, path: str, methods: list[str], handler: Callable) -> None:
        """Add a route to the FastAPI application"""
        # FastAPI uses add_api_route for dynamic route registration
        # Convert methods to uppercase as FastAPI expects
        methods_upper = [method.upper() for method in methods]

        # Wrap the handler to pass the request object and handle sync/async
        async def wrapped_handler(request: Request):
            import asyncio

            # If handler is async, await it; if sync, run in executor
            if asyncio.iscoroutinefunction(handler):
                return await handler(request)
            else:
                # Run synchronous handler in executor
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, handler, request)

        self.app.add_api_route(path, wrapped_handler, methods=methods_upper)

    def run(self, host: str, port: int, debug: bool) -> None:
        """Run the FastAPI application"""
        import uvicorn

        uvicorn.run(self.app, host=host, port=port, reload=False)

    def create_response(self, data: Dict[str, Any], status_code: int = 200) -> JSONResponse:
        """Create a FastAPI response"""
        return JSONResponse(content=data, status_code=status_code)

    def get_request_data(self) -> Dict[str, Any]:
        """Get data from the FastAPI request"""
        # This would need to be called within a request context
        return {}

    def get_json_data(self, request) -> Dict[str, Any]:
        """Get JSON data from FastAPI request"""
        try:
            # For FastAPI, we need to get the JSON data from the request body
            if hasattr(request, "json") and callable(getattr(request, "json")):
                # Handle both sync and async json methods
                if hasattr(request.json, "__await__"):
                    # Async json method
                    import asyncio

                    return asyncio.run(request.json())
                else:
                    # Sync json method
                    return request.json()
            return {}
        except Exception:
            return {}
