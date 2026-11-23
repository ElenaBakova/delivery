from dataclasses import dataclass


@dataclass(frozen=True)
class Volume:
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("volume must be positive")
