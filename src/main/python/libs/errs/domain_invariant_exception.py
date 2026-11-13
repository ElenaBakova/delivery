from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .error import Error


class DomainInvariantException(RuntimeError):
    def __init__(self, error: "Error") -> None:
        super().__init__(f"Domain invariant violated: {error.message}")
