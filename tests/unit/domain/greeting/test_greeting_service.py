from datetime import datetime
from unittest.mock import patch

import pytest
from injector import Injector

from domain import (
    GreetingLanguage,
    GreetingService,
    GreetingType,
    PersonName,
)
from infrastructure import GreetingModule


class TestGreetingService:
    @pytest.fixture
    def injector(self):
        return Injector([GreetingModule])

    def test_get_greeting_message_basic_en(self, injector: Injector):
        greeting_service = injector.get(GreetingService)

        first_name = "Alice"
        last_name = "Smith"
        greeting_type = GreetingType.BASIC
        greeting_language = GreetingLanguage.EN
        greeting_message = greeting_service.get_greeting_message(
            PersonName(first_name=first_name, last_name=last_name), greeting_type, greeting_language
        )

        assert f"{first_name} {last_name}" in greeting_message
        assert "Hello" in greeting_message

    @patch("domain.greeting.greeting_strategies.time_based_greeting_strategy.datetime")
    def test_get_greeting_message_timebased_fr(self, mock_datetime, injector: Injector):
        mock_now = datetime(2024, 12, 10, 9, 0, 0)

        mock_datetime.datetime.now.return_value = mock_now

        greeting_service = injector.get(GreetingService)

        first_name = "Bob"
        last_name = "Doe"
        greeting_type = GreetingType.TIME_BASED
        greeting_language = GreetingLanguage.FR
        greeting_message = greeting_service.get_greeting_message(
            PersonName(first_name=first_name, last_name=last_name), greeting_type, greeting_language
        )

        assert f"{first_name} {last_name}" in greeting_message
        assert "Bonjour" in greeting_message

    @patch("domain.greeting.greeting_strategies.holiday_greeting_strategy.datetime")
    def test_get_greeting_message_holiday_es(self, mock_datetime, injector: Injector):
        mock_now = datetime(2024, 12, 25, 10, 0, 0)
        mock_datetime.datetime.now.return_value = mock_now

        greeting_service = injector.get(GreetingService)

        first_name = "Charlie"
        last_name = "Brown"
        greeting_type = GreetingType.HOLIDAY
        greeting_language = GreetingLanguage.ES
        greeting_message = greeting_service.get_greeting_message(
            PersonName(first_name=first_name, last_name=last_name), greeting_type, greeting_language
        )

        assert f"{first_name} {last_name}" in greeting_message
        assert "Feliz Navidad" in greeting_message
