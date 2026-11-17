from dataclasses import dataclass

from .domain_invariant_exception import DomainInvariantException


@dataclass(frozen=True, init=False, eq=False)
class Error:
    code: str
    message: str

    def __init__(self, code: str | None, message: str | None) -> None:
        if code is None or message is None:
            raise ValueError("Code and message must not be None")
        object.__setattr__(self, "code", code)
        object.__setattr__(self, "message", message)

    @classmethod
    def of(cls, code: str | None, message: str | None) -> "Error":
        return cls(code, message)

    def serialize(self) -> str:
        return f"{self.code}||{self.message}"

    @classmethod
    def deserialize(cls, serialized: str) -> "Error":
        from .general_errors import GeneralErrors

        if serialized == "A non-empty request body is required.":
            return GeneralErrors.value_is_required("serialized")
        parts = serialized.split("||")
        if len(parts) < 2:
            raise ValueError(f"Invalid error serialization: '{serialized}'")
        return cls(parts[0], parts[1])

    @staticmethod
    def throw_if(error: "Error | None") -> None:
        if error is not None:
            raise DomainInvariantException(error)

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, Error):
            return False
        return self.code == other.code and self.message == other.message

    def __hash__(self) -> int:
        return hash((self.code, self.message))

    def __str__(self) -> str:
        return f"Error{{code='{self.code}', message='{self.message}'}}"
