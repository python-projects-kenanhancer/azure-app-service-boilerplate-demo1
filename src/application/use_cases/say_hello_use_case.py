from injector import inject

# Domain models and services
from domain import GreetingService, PersonName
from infrastructure import LoggerStrategy, Settings

# Application-layer DTOs
from ..dtos import GreetingAppRequest, GreetingAppResponse


class SayHelloUseCase:
    """
    Coordinates the "say hello" operation.

    Responsibilities:
    1) Convert input DTO -> domain model (PersonName).
    2) Configure domain services (GreetingService) using domain settings.
    3) Execute domain logic to produce a greeting message.
    4) Return output as a DTO (GreetingResponse).

    This layer doesn't handle HTTP or external frameworks;
    it just orchestrates domain logic using domain models/services.
    """

    @inject
    def __init__(self, say_hello_settings: Settings, greeting_service: GreetingService, logger: LoggerStrategy):
        self.logger = logger
        self.say_hello_settings = say_hello_settings
        self.greeting_service = greeting_service

    def execute(self, request_app: GreetingAppRequest) -> GreetingAppResponse:
        person_name = PersonName.model_validate(request_app.to_dict())

        greeting_type = self.say_hello_settings.greeting_type
        greeting_language = self.say_hello_settings.greeting_language

        greeting_message = self.greeting_service.get_greeting_message(person_name, greeting_type, greeting_language)

        self.logger.info("Final greeting to user: %s", greeting_message)

        return GreetingAppResponse(message=greeting_message)
