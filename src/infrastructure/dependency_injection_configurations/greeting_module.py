from injector import Binder, Module, singleton

from domain import BasicGreetingStrategy, GreetingType, HolidayGreetingStrategy, TimeBasedGreetingStrategy


class GreetingModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(GreetingType.BASIC.value, to=BasicGreetingStrategy, scope=singleton)
        binder.bind(GreetingType.HOLIDAY.value, to=HolidayGreetingStrategy, scope=singleton)
        binder.bind(GreetingType.TIME_BASED.value, to=TimeBasedGreetingStrategy, scope=singleton)
