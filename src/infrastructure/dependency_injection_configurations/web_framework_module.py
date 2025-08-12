from injector import Module, provider, singleton

from ..web_apps.fastapi_web_app import FastAPIWebApp
from ..web_apps.flask_web_app import FlaskWebApp
from ..web_apps.web_app_interface import WebAppInterface
from .settings_module import Settings


class WebFrameworkModule(Module):
    """Dependency injection module for web framework selection"""

    @singleton
    @provider
    def provide_web_app(self, settings: Settings) -> WebAppInterface:
        """Provide the appropriate web application based on configuration"""

        # Use settings.web_framework from the config loader
        framework = settings.web_framework.lower()

        if framework == "fastapi":
            return FastAPIWebApp()
        elif framework == "flask":
            return FlaskWebApp()
        else:
            raise ValueError(f"Unsupported web framework: {framework}. Supported: flask, fastapi")
