from collections.abc import Iterable
from typing import Any, Protocol

from .aggregate import Aggregate


class DomainEventPublisher(Protocol):
    def publish(self, aggregates: Iterable[Aggregate[Any]]) -> None: ...
