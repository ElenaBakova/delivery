from collections.abc import Callable
from typing import Generic, TypeVar, cast, overload

from .domain_invariant_exception import DomainInvariantException
from .error import Error

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E", bound=Error)
F = TypeVar("F", bound=Error)
_MISSING = object()


class Result(Generic[T, E]):
    def __init__(self, value: T | None, error: E | None, is_success: bool) -> None:
        if is_success and error is not None or not is_success and error is None:
            raise ValueError("Invalid result state")
        self._value = value
        self._error = error
        self._is_success = is_success

    @overload
    @classmethod
    def success(cls) -> "Result[None, E]": ...

    @overload
    @classmethod
    def success(cls, value: U) -> "Result[U, E]": ...

    @classmethod
    def success(
        cls, value: U | object = _MISSING
    ) -> "Result[U, E] | Result[None, E]":
        if value is _MISSING:
            return Result[None, E](None, None, True)
        if value is None:
            raise ValueError("Value must not be None")
        return Result[U, E](cast(U, value), None, True)

    @classmethod
    def failure(cls, error: E | None) -> "Result[T, E]":
        if error is None:
            raise ValueError("Error must not be None on failure")
        return cls(None, error, False)

    @property
    def is_success(self) -> bool:
        return self._is_success

    @property
    def is_failure(self) -> bool:
        return not self.is_success

    @property
    def value(self) -> T:
        if self.is_failure:
            raise RuntimeError("Cannot get value from failure")
        return cast(T, self._value)

    @property
    def error(self) -> E:
        if self.is_success:
            raise RuntimeError("Cannot get error from success")
        return cast(E, self._error)

    def map(self, mapper: Callable[[T], U]) -> "Result[U, E]":
        return Result.success(mapper(self.value)) if self.is_success else Result.failure(self.error)

    def flat_map(self, mapper: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        return mapper(self.value) if self.is_success else Result.failure(self.error)

    def on_success(self, handler: Callable[[T], None]) -> "Result[T, E]":
        if self.is_success:
            handler(self.value)
        return self

    def on_failure(self, handler: Callable[[E], None]) -> "Result[T, E]":
        if self.is_failure:
            handler(self.error)
        return self

    def fold(self, on_success: Callable[[T], U], on_failure: Callable[[E], U]) -> U:
        return on_success(self.value) if self.is_success else on_failure(self.error)

    def map_error(self, mapper: Callable[[E], F]) -> "Result[T, F]":
        if self.is_failure:
            return Result.failure(mapper(self.error))
        return Result.success(self.value)

    def get_value_or_throw(self) -> T:
        """Fail fast only where failure is impossible by the domain contract."""
        if self.is_failure:
            raise DomainInvariantException(self.error)
        return self.value

    def __str__(self) -> str:
        if self.is_failure:
            return f"Failure({self.error})"
        value = self.value
        formatted = (
            "null" if value is None
            else str(value).lower() if isinstance(value, bool)
            else str(value)
        )
        return f"Success({formatted})"
