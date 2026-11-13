from collections.abc import Collection
from typing import Protocol, Self, TypeVar, final
from unicodedata import category
from uuid import UUID

from .error import Error
from .general_errors import GeneralErrors


class _Comparable(Protocol):
    def __lt__(self, other: Self, /) -> bool: ...
    def __le__(self, other: Self, /) -> bool: ...
    def __gt__(self, other: Self, /) -> bool: ...
    def __ge__(self, other: Self, /) -> bool: ...


T = TypeVar("T", bound=_Comparable)


def _is_blank(value: str) -> bool:
    # Character.isWhitespace excludes non-breaking spaces, unlike str.isspace.
    return all(
        character in "\t\n\v\f\r\x1c\x1d\x1e\x1f"
        or category(character) in {"Zs", "Zl", "Zp"}
        and character not in "\u00a0\u2007\u202f"
        for character in value
    )


@final
class Guard:
    def __new__(cls) -> Self:
        raise TypeError("Guard is a utility class and cannot be instantiated")

    @staticmethod
    def combine(*errors: Error | None) -> Error | None:
        return next((error for error in errors if error is not None), None)

    @staticmethod
    def against_null_or_empty(
        value: str | Collection[object] | UUID | None, param_name: str | None
    ) -> Error | None:
        if (
            value is None
            or isinstance(value, str)
            and _is_blank(value)
            or isinstance(value, UUID)
            and value.int == 0
            or isinstance(value, Collection)
            and len(value) == 0
        ):
            return GeneralErrors.value_is_required(param_name)
        return None

    @staticmethod
    def against_greater_than(
        value: T | None, maximum: T, param_name: str | None
    ) -> Error | None:
        if value is None or value > maximum:
            return GeneralErrors.value_must_be_less_than(param_name, value, maximum)
        return None

    @staticmethod
    def against_greater_or_equal(
        value: T | None, maximum: T, param_name: str | None
    ) -> Error | None:
        if value is None or value >= maximum:
            return GeneralErrors.value_must_be_less_or_equal(param_name, value, maximum)
        return None

    @staticmethod
    def against_less_than(
        value: T | None, minimum: T, param_name: str | None
    ) -> Error | None:
        if value is None or value < minimum:
            return GeneralErrors.value_must_be_less_than(param_name, value, minimum)
        return None

    @staticmethod
    def against_less_or_equal(
        value: T | None, minimum: T, param_name: str | None
    ) -> Error | None:
        if value is None or value <= minimum:
            return GeneralErrors.value_must_be_greater_or_equal(
                param_name, value, minimum
            )
        return None

    @staticmethod
    def against_out_of_range(
        value: T | None, minimum: T, maximum: T, param_name: str | None
    ) -> Error | None:
        if value is None or value < minimum or value > maximum:
            return GeneralErrors.value_is_out_of_range(
                param_name, value, minimum, maximum
            )
        return None
