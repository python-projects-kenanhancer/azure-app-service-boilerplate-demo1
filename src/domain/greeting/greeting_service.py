from typing import cast

from injector import Injector, inject

from .greeting_language_decorator import GreetingLanguageDecorator
from .greeting_strategies import GreetingStrategy
from .models import GreetingLanguage, GreetingType, PersonName


class GreetingService:
    @inject
    def __init__(self, injector: Injector):
        self._injector = injector

    def get_greeting_message(self, person_name: PersonName, greeting_type: GreetingType, greeting_language: GreetingLanguage):

        # 1) Create the base greeting strategy (in English)
        greeting_strategy = cast(GreetingStrategy, self._injector.get(greeting_type.value))

        # 2) Wrap it with the greeting language decorator
        greeting_decorated_strategy = GreetingLanguageDecorator(
            base_greeting_strategy=greeting_strategy, language=greeting_language
        )

        # 3) Generate the final prefix
        greeting_prefix = greeting_decorated_strategy.get_greeting_prefix()

        # 4) Combine with the user's name
        full_name = f"{person_name.first_name} {person_name.last_name}"

        return f"{greeting_prefix} {full_name}!"
