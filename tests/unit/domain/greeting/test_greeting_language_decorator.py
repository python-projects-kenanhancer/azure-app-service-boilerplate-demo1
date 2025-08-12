from unittest.mock import MagicMock

import pytest

from domain import GreetingLanguageDecorator, GreetingStrategy


class TestGreetingLanguageDecorator:
    @pytest.mark.parametrize(
        "base_greeting_prefix, language, expected_greeting_prefix",
        [
            ("Hello", "en", "Hello"),
            ("Hello", "fr", "Salut"),
            ("Hello", "es", "Hola"),
            ("Good morning", "fr", "Bonjour"),
            ("Good evening", "es", "Buenas noches"),
            ("RandomPhrase", "fr", "RandomPhrase"),  # fallback
        ],
    )
    def test_language_decorator(self, base_greeting_prefix, language, expected_greeting_prefix):
        mock_greeting_strategy = MagicMock(spec=GreetingStrategy)

        mock_greeting_strategy.get_greeting_prefix.return_value = base_greeting_prefix

        greeting_language_decorator = GreetingLanguageDecorator(mock_greeting_strategy, language=language)

        greeting_prefix = greeting_language_decorator.get_greeting_prefix()

        assert greeting_prefix == expected_greeting_prefix
