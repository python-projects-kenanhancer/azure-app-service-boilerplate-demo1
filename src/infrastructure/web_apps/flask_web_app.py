from typing import Callable

from flask import Flask, jsonify, request

from .web_app_interface import WebAppInterface


class FlaskWebApp(WebAppInterface):
    """Flask implementation of the WebAppInterface"""

    def __init__(self):
        self.app = Flask(__name__)

    def add_route(self, path: str, methods: list[str], handler: Callable) -> None:
        """Add a route to the Flask application"""
        # Wrap the handler to pass the request object for consistency with FastAPI
        # Use a unique endpoint name based on the path to avoid conflicts
        endpoint_name = f"endpoint_{path.replace('/', '_').replace('-', '_')}"

        def wrapped_handler():
            return handler(request)

        self.app.route(path, methods=methods, endpoint=endpoint_name)(wrapped_handler)

    def run(self, host: str, port: int, debug: bool) -> None:
        """Run the Flask application"""
        self.app.run(host=host, port=port, debug=debug)

    def create_response(self, data: dict, status_code: int = 200) -> tuple:
        """Create a Flask response"""
        return jsonify(data), status_code

    def get_request_data(self) -> dict:
        """Get data from the Flask request"""
        return request.get_json() or {}

    def get_json_data(self, request) -> dict:
        """Get JSON data from Flask request"""
        return request.get_json() or {}


def create_flask_app() -> Flask:
    """Create and configure the Flask application"""
    web_app = FlaskWebApp()
    return web_app.app
