from injector import inject

from application import GreetingAppRequest, SayHelloUseCase
from infrastructure import LoggerStrategy, WebAppInterface, pipeline, shared_pipeline
from interfaces import GreetingHttpRequest, GreetingHttpResponse


class GreetingController:
    """Controller for greeting-related endpoints"""

    @inject
    def __init__(self, web_app: WebAppInterface, say_hello_use_case: SayHelloUseCase, logger: LoggerStrategy):
        self.web_app = web_app
        self.say_hello_use_case = say_hello_use_case
        self.logger = logger
        self._setup_routes()

    def _setup_routes(self):
        self.web_app.add_route("/say_hello", ["POST"], self._handle_say_hello)
        self.web_app.add_route("/health", ["GET"], self._handle_health_check)

    @pipeline(shared_pipeline)
    def _handle_say_hello(self, request: GreetingHttpRequest):
        request_app: GreetingAppRequest = GreetingAppRequest.model_validate(request.to_dict())

        greeting_message = self.say_hello_use_case.execute(request_app)

        self.logger.info(greeting_message.message)

        return GreetingHttpResponse.model_validate(greeting_message.to_dict())

        # return self.web_app.create_response(greeting_message.model_dump(), 200)

    @pipeline(shared_pipeline)
    def _handle_health_check(self, request):
        return self.web_app.create_response({"status": "healthy"}, 200)
