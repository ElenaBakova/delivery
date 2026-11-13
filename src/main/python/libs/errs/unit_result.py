from collections.abc import Callable
from typing import Generic, TypeVar, cast, final

from .domain_invariant_exception import DomainInvariantException
from .error import Error
from .result import Result

E = TypeVar("E", bound=Error)
U = TypeVar("U")


@final
class UnitResult(Generic[E]):
    def __init__(self, is_success: bool, error: E | None = None) -> None:
        if is_success and error is not None or not is_success and error is None:
            raise ValueError("Invalid result state")
        self._is_success = is_success
        self._error = error

    @classmethod
    def success(cls) -> "UnitResult[E]":
        return cls(True)

    @classmethod
    def failure(cls, error: E | None) -> "UnitResult[E]":
        if error is None:
            raise ValueError("Error must not be null on failure")
        return cls(False, error)

    @property
    def is_success(self) -> bool:
        return self._is_success

    @property
    def is_failure(self) -> bool:
        return not self.is_success

    @property
    def error(self) -> E:
        if self.is_success:
            raise RuntimeError("Cannot get error from success")
        return cast(E, self._error)

    def on_success(self, handler: Callable[[], None]) -> "UnitResult[E]":
        if self.is_success:
            handler()
        return self

    def on_failure(self, handler: Callable[[E], None]) -> "UnitResult[E]":
        if self.is_failure:
            handler(self.error)
        return self

    def fold(self, on_success: Callable[[None], U], on_failure: Callable[[E], U]) -> U:
        return on_success(None) if self.is_success else on_failure(self.error)

    def merge(self, other: "UnitResult[E]") -> "UnitResult[E]":
        if self.is_failure:
            return self
        if other.is_failure:
            return other
        return UnitResult.success()

    @classmethod
    def from_result(cls, result: Result[None, E]) -> "UnitResult[E]":
        return cls.success() if result.is_success else cls.failure(result.error)

    def to_result(self) -> Result[None, E]:
        return Result.success() if self.is_success else Result.failure(self.error)

    def get_or_else_throw(self, exception_mapper: Callable[[E], Exception] = DomainInvariantException) -> None:
        """Without a mapper, fail fast only where failure violates the domain contract."""
        if self.is_failure:
            raise exception_mapper(self.error)

    def __str__(self) -> str:
        return "Success" if self.is_success else f"Failure({self.error})"
