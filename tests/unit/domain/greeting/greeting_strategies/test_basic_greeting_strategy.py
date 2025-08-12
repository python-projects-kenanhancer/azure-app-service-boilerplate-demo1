from domain import BasicGreetingStrategy


class TestBasicGreetingStrategy:

    def test_get_greeting_prefix(self):
        greeting_strategy = BasicGreetingStrategy()

        greeting_prefix = greeting_strategy.get_greeting_prefix()

        expected_greeting_prefix = "Hello"

        assert greeting_prefix == expected_greeting_prefix
