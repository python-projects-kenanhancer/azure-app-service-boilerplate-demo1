from .greeting_strategies import GreetingStrategy
from .models import GreetingLanguage


class GreetingLanguageDecorator(GreetingStrategy):
    """
    Wraps another GreetingStrategy and translates its English-based prefix
    into the specified language, if available.
    """

    def __init__(self, base_greeting_strategy: GreetingStrategy, language: GreetingLanguage):
        self.base_greeting_strategy = base_greeting_strategy
        self.language = language

    def get_greeting_prefix(self) -> str:
        # 1) Get the 'raw' greeting prefix in English (or a base language)
        raw_prefix = self.base_greeting_strategy.get_greeting_prefix()
        # 2) Translate/localize that prefix into the chosen language
        return self._localize(raw_prefix, self.language)

    def _localize(self, english_prefix: str, language: str) -> str:
        """
        Very simple translation logic. You would typically have a real i18n tool
        or dictionary of translations. We'll just map a few examples.
        """
        translations = {
            "en": {
                "Hello": "Hello",
                "Good morning": "Good morning",
                "Good afternoon": "Good afternoon",
                "Good evening": "Good evening",
                "Merry Christmas": "Merry Christmas",
                "Happy Holidays": "Happy Holidays",
                "Hey there": "Hey there",
                "Howdy": "Howdy",
                "What's up": "What's up",
                "Ahoy": "Ahoy",
                "Greetings": "Greetings",
            },
            "fr": {
                "Hello": "Salut",
                "Good morning": "Bonjour",
                "Good afternoon": "Bon après-midi",
                "Good evening": "Bonjour",
                "Merry Christmas": "Joyeux Noël",
                "Happy Holidays": "Joyeuses Fêtes",
                "Hey there": "Coucou",
                "Howdy": "Salut",
                "What's up": "Ça va?",
                "Ahoy": "Ohé",
                "Greetings": "Salutations",
            },
            "es": {
                "Hello": "Hola",
                "Good morning": "Buenos días",
                "Good afternoon": "Buenas tardes",
                "Good evening": "Buenas noches",
                "Merry Christmas": "Feliz Navidad",
                "Happy Holidays": "Felices Fiestas",
                "Hey there": "Buenas",
                "Howdy": "Hola",
                "What's up": "¿Qué tal?",
                "Ahoy": "Ahoy (Español?)",
                "Greetings": "Saludos",
            },
            # Add more languages as needed
        }

        # Fallback if language or phrase not found
        if language not in translations:
            # Default back to English
            return english_prefix

        localized_dict = translations[language]
        return localized_dict.get(english_prefix, english_prefix)
