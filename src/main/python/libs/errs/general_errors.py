from typing import Self, final

from .error import Error

_JAVA_TRIM_CHARS = "".join(chr(code) for code in range(33))


def _name(name: str | None) -> str:
    if name is None or not name.strip(_JAVA_TRIM_CHARS):
        raise ValueError("Name must not be null or empty")
    return name


def _string(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


@final
class GeneralErrors:
    def __new__(cls) -> Self:
        raise TypeError("GeneralErrors is a utility class and cannot be instantiated")

    @staticmethod
    def not_found(name: str | None, id: object) -> Error:
        name = _name(name)
        return Error.of("record.not.found", f"Record not found. Name: {name}, id: {_string(id)}")

    @staticmethod
    def value_is_invalid(name: str | None, value: object) -> Error:
        name = _name(name)
        return Error.of("value.is.invalid", f"Value '{_string(value)}' is invalid for {name}")

    @staticmethod
    def value_is_required(name: str | None) -> Error:
        name = _name(name)
        return Error.of("value.is.required", f"Value is required for {name}")

    @staticmethod
    def invalid_length(name: str | None) -> Error:
        name = _name(name)
        return Error.of("invalid.string.length", f"Invalid {name} length")

    @staticmethod
    def collection_is_too_small(minimum: int, current: int) -> Error:
        return Error.of(
            "collection.is.too.small",
            f"The collection must contain {minimum} items or more. It contains {current} items.",
        )

    @staticmethod
    def collection_is_too_large(maximum: int, current: int) -> Error:
        return Error.of(
            "collection.is.too.large",
            f"The collection must contain {maximum} items or fewer. It contains {current} items.",
        )

    @staticmethod
    def value_is_out_of_range(name: str | None, value: object, minimum: object, maximum: object) -> Error:
        name = _name(name)
        return Error.of(
            "value.is.out.of.range",
            f"Value {_string(value)} for {name} is out of range. "
            f"Min value is {_string(minimum)}, max value is {_string(maximum)}.",
        )

    @staticmethod
    def value_must_be_greater_than(name: str | None, value: object, minimum: object) -> Error:
        name = _name(name)
        return Error.of(
            "value.must.be.greater.than",
            f"The value of {name} ({_string(value)}) must be greater than {_string(minimum)}.",
        )

    @staticmethod
    def value_must_be_greater_or_equal(name: str | None, value: object, minimum: object) -> Error:
        name = _name(name)
        return Error.of(
            "value.must.be.greater.or.equal",
            f"The value of {name} ({_string(value)}) must be greater than or equal to {_string(minimum)}.",
        )

    @staticmethod
    def value_must_be_less_than(name: str | None, value: object, maximum: object) -> Error:
        name = _name(name)
        return Error.of(
            "value.must.be.less.than",
            f"The value of {name} ({_string(value)}) must be less than {_string(maximum)}.",
        )

    @staticmethod
    def value_must_be_less_or_equal(name: str | None, value: object, maximum: object) -> Error:
        name = _name(name)
        return Error.of(
            "value.must.be.less.or.equal",
            f"The value of {name} ({_string(value)}) must be less than or equal to {_string(maximum)}.",
        )
