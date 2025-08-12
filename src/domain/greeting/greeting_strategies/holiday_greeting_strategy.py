import datetime

from .greeting_strategy import GreetingStrategy


class HolidayGreetingStrategy(GreetingStrategy):
    """Returns holiday-themed greetings in December, otherwise 'Hello'."""

    def get_greeting_prefix(self) -> str:
        now = datetime.datetime.now()
        # Very simplistic holiday logic:
        if now.month == 12 and now.day == 25:
            return "Merry Christmas"
        elif now.month == 12:
            return "Happy Holidays"
        else:
            return "Hello"  # Fallback if not December
