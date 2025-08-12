from datetime import datetime
from unittest.mock import patch

import pytest

from domain import TimeBasedGreetingStrategy


class TestTimeBasedGreetingStrategy:
    @pytest.mark.parametrize(
        "hour,expected_greeting_prefix",
        [
            (6, "Good morning"),
            (11, "Good morning"),
            (12, "Good afternoon"),
            (17, "Good afternoon"),
            (19, "Good evening"),
            (23, "Good evening"),
        ],
    )
    def test_get_greeting_prefix_various_times(self, hour, expected_greeting_prefix):
        greeting_strategy = TimeBasedGreetingStrategy()

        with patch("domain.greeting.greeting_strategies.time_based_greeting_strategy.datetime") as mock_datetime:
            # 1) Create a *real* datetime object for your desired hour
            real_dt = datetime(2024, 12, 25, hour, 0, 0)

            # 2) Make sure that whenever code calls `datetime.datetime.now()`,
            mock_datetime.datetime.now.return_value = real_dt

            greeting_prefix = greeting_strategy.get_greeting_prefix()

            assert greeting_prefix == expected_greeting_prefix
