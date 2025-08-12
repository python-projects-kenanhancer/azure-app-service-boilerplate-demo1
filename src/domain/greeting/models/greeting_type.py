from enum import Enum
from typing import NewType

basic = NewType("basic", str)
time_based = NewType("time_based", str)
holiday = NewType("holiday", str)


class GreetingType(str, Enum):
    BASIC = basic
    TIME_BASED = time_based
    HOLIDAY = holiday

    @classmethod
    def _missing_(cls, value):
        if not isinstance(value, str):
            raise ValueError(f"Invalid type for greeting_type: {value!r}")
        # Lowercase or do your own logic
        key = value.lower()

        # Build a map from the NewType.__name__ -> enum member
        # e.g. "time_based" -> GreetingType.TIME_BASED
        lookup = {member._name_.lower(): member for member in cls}
        # In the above, member.value is e.g. time_based("time_based")
        # so member.value.__name__ -> "time_based"

        if key in lookup:
            return lookup[key]

        raise ValueError(f"Unrecognized greeting_type: {value!r}")


__all__ = ["GreetingType", "basic", "time_based", "holiday"]
