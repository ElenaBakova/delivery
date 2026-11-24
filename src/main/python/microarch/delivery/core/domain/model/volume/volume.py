from dataclasses import dataclass

from typing_extensions import Self


@dataclass(frozen=True)
class Volume:
    value: int

    def __post_init__(self):
        if self.value is not int:
            raise TypeError("volume must be integer")

        if self.value <= 0:
            raise ValueError("volume must be positive")

    def __add__(self, other: Self) -> "Volume":
        if not isinstance(other, Volume):
            raise TypeError("types are incompitable")

        return Volume(self.value + other.value)

    def __lt__(self, other: Self) -> bool:
        if not isinstance(other, Volume):
            raise TypeError("types are incompitable")

        return self.value < other.value

    def __le__(self, other: Self) -> bool:
        if not isinstance(other, Volume):
            raise TypeError("types are incompitable")

        return self.value <= other.value

    def __gt__(self, other: Self) -> bool:
        if not isinstance(other, Volume):
            raise TypeError("types are incompitable")

        return self.value > other.value

    def __ge__(self, other: Self) -> bool:
        if not isinstance(other, Volume):
            raise TypeError("types are incompitable")

        return self.value >= other.value
