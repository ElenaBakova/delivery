from typing import List

from .base_entity import BaseEntity, TId
from .domain_event import DomainEvent


class Aggregate(BaseEntity[TId]):
    def __init__(self, id: TId | None = None) -> None:
        super().__init__(id)
        self._domain_events: list[DomainEvent] = []

    @property
    def domain_events(self) -> List[DomainEvent]:
        return list(self._domain_events)

    def clear_domain_events(self) -> None:
        self._domain_events.clear()

    def raise_domain_event(self, domain_event: DomainEvent) -> None:
        self._domain_events.append(domain_event)
