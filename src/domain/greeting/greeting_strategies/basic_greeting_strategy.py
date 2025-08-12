from .greeting_strategy import GreetingStrategy


class BasicGreetingStrategy(GreetingStrategy):
    """Always returns 'Hello'."""

    def get_greeting_prefix(self) -> str:
        return "Hello"
