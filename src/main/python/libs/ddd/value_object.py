from abc import ABC, abstractmethod
from collections.abc import Iterable
from decimal import Decimal
from typing import Any, Self


class ValueObject(ABC):
    @abstractmethod
    def equality_components(self) -> Iterable[Any]: ...

    @staticmethod
    def safe_compare(a: Any, b: Any) -> int:
        if a is b:
            return 0
        if a is None:
            return -1
        if b is None:
            return 1
        if isinstance(a, Decimal) and isinstance(b, Decimal):
            return (a > b) - (a < b)
        try:
            return (a > b) - (a < b)
        except TypeError as exception:
            raise ValueError("Fields must be Comparable") from exception

    @staticmethod
    def _components_equal(a: object, b: object) -> bool:
        if isinstance(a, Decimal) and isinstance(b, Decimal):
            # BigDecimal.equals compares both numerical value and scale.
            return a == b and a.as_tuple().exponent == b.as_tuple().exponent
        return a == b

    @staticmethod
    def _component_hash(component: Any) -> int:
        if isinstance(component, Decimal):
            return hash((component, component.as_tuple().exponent))
        return hash(component)

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, ValueObject) or type(self) is not type(other):
            return False
        left = list(self.equality_components())
        right = list(other.equality_components())
        if len(left) != len(right):
            return False
        return all(self._components_equal(a, b) for a, b in zip(left, right))

    def __hash__(self) -> int:
        return hash(tuple(self._component_hash(component) for component in self.equality_components()))

    def compare_to(self, other: Self) -> int:
        left, right = (
            list(self.equality_components()),
            list(other.equality_components()),
        )
        for a, b in zip(left, right):
            result = self.safe_compare(a, b)
            if result:
                return result
        return (len(left) > len(right)) - (len(left) < len(right))

    def __lt__(self, other: Self) -> bool:
        return self.compare_to(other) < 0

    def __le__(self, other: Self) -> bool:
        return self.compare_to(other) <= 0

    def __gt__(self, other: Self) -> bool:
        return self.compare_to(other) > 0

    def __ge__(self, other: Self) -> bool:
        return self.compare_to(other) >= 0

    def __str__(self) -> str:
        components = list(self.equality_components())
        formatted = (
            "null" if component is None
            else str(component).lower() if isinstance(component, bool)
            else str(component)
            for component in components
        )
        return f"{type(self).__name__}[{', '.join(formatted)}]"
