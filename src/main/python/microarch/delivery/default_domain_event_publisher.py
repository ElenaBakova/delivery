from collections.abc import Iterable
from typing import Any, Protocol

from libs.ddd import Aggregate, DomainEvent


class ApplicationEventPublisher(Protocol):
    def publish_event(self, event: DomainEvent) -> None: ...


class DefaultDomainEventPublisher:
    def __init__(self, publisher: ApplicationEventPublisher) -> None:
        self.publisher = publisher

    def publish(self, aggregates: Iterable[Aggregate[Any]]) -> None:
        for aggregate in aggregates:
            for event in aggregate.domain_events:
                self.publisher.publish_event(event)
