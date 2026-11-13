from typing import Protocol, TypeVar

from .domain_event import DomainEvent

TId_co = TypeVar("TId_co", covariant=True)


class AggregateRoot(Protocol[TId_co]):
    @property
    def id(self) -> TId_co | None: ...

    @property
    def domain_events(self) -> tuple[DomainEvent, ...]: ...

    def clear_domain_events(self) -> None: ...
