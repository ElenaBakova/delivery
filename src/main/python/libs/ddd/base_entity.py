from functools import total_ordering
from typing import Generic, Protocol, Self, TypeVar, cast


class Comparable(Protocol):
    def __lt__(self, other: Self, /) -> bool: ...


TId = TypeVar("TId", bound=Comparable)


@total_ordering
class BaseEntity(Generic[TId]):
    def __init__(self, id: TId | None = None) -> None:
        self.id = id

    def default_value(self) -> TId | None:
        return None

    def is_transient(self) -> bool:
        return self.id is None or self.id == self.default_value()

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if type(self) is not type(other):
            return False
        other_entity = cast("BaseEntity[TId]", other)
        return (
            not self.is_transient()
            and not other_entity.is_transient()
            and self.id == other_entity.id
        )

    def __hash__(self) -> int:
        return hash((type(self), self.id))

    def compare_to(self, other: "BaseEntity[TId] | None") -> int:
        if other is None:
            return 1
        if self is other:
            return 0
        left, right = self.id, other.id
        if left is None or right is None:
            raise TypeError("Cannot compare entities without IDs")
        return (right < left) - (left < right)

    def __lt__(self, other: "BaseEntity[TId]") -> bool:
        return self.compare_to(other) < 0
