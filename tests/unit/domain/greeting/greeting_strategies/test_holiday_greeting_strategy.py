from datetime import datetime
from unittest.mock import patch

import pytest

from domain import HolidayGreetingStrategy


class TestHolidayGreetingStrategy:
    @pytest.mark.parametrize(
        "month,day,expected_greeting_prefix",
        [
            (12, 25, "Merry Christmas"),
            (12, 10, "Happy Holidays"),
            (11, 25, "Hello"),
        ],
    )
    def test_get_greeting_prefix_various_dates(self, month, day, expected_greeting_prefix):
        greeting_strategy = HolidayGreetingStrategy()

        with patch("domain.greeting.greeting_strategies.holiday_greeting_strategy.datetime") as mock_datetime:
            # 1) Create a *real* datetime object for your desired hour
            real_dt = datetime(2024, month, day, 10, 0, 0)

            # 2) Make sure that whenever code calls `datetime.datetime.now()`,
            mock_datetime.datetime.now.return_value = real_dt

            greeting_prefix = greeting_strategy.get_greeting_prefix()

            assert greeting_prefix == expected_greeting_prefix
