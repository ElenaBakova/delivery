from dataclasses import dataclass

from typing_extensions import Self

MIN_LOCATION = 1
MAX_LOCATION = 10


@dataclass(frozen=True)
class Location:
    x: int
    y: int

    @staticmethod
    def _is_valid_coordinate(value: int, name: str) -> bool:
        if type(value) is not int:
            raise TypeError(f"{name} must be an integer")
        if value not in range(MIN_LOCATION, MAX_LOCATION + 1):
            raise ValueError(
                f"{name} must be in range [{MIN_LOCATION}, {MAX_LOCATION}]"
            )
        return True

    def __post_init__(self):
        for name, value in (("X", self.x), ("Y", self.y)):
            self._is_valid_coordinate(value, name)

    def distance(self, destination: Self):
        return abs(self.x - destination.x) + abs(self.y - destination.y)
