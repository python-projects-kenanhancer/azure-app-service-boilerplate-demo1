import datetime

from .greeting_strategy import GreetingStrategy


class TimeBasedGreetingStrategy(GreetingStrategy):
    """Returns 'Good morning', 'Good afternoon', or 'Good evening' depending on the current hour."""

    def get_greeting_prefix(self) -> str:
        now_hour = datetime.datetime.now().hour
        if 5 <= now_hour < 12:
            return "Good morning"
        elif 12 <= now_hour < 18:
            return "Good afternoon"
        else:
            return "Good evening"
