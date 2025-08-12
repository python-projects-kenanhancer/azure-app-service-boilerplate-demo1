from injector import inject, singleton

from infrastructure import LoggerStrategy

from ..http import AuthController, AuthenticatedController, GreetingController


@singleton
class ApplicationBootstrap:
    """Bootstrap class that initializes controllers by injecting them."""

    @inject
    def __init__(
        self,
        greeting_controller: GreetingController,
        authenticated_controller: AuthenticatedController,
        auth_controller: AuthController,
        logger: LoggerStrategy,
    ):
        self.controllers = [greeting_controller, authenticated_controller, auth_controller]
        self.logger = logger

    def build(self):
        """Build and initialize the application.

        This method is called from main to ensure controllers are properly initialized
        and their routes are registered before the web server starts.
        """
        # Controllers are instantiated just by being injected in __init__
        # Their __init__ methods will register routes automatically
        self.logger.info(
            f"✅ Controllers initialized: {type(self.controllers[0]).__name__}, {type(self.controllers[1]).__name__}, {type(self.controllers[2]).__name__}"
        )

        self.logger.info("🚀 Application bootstrap completed successfully")

        return self
