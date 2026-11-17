from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass(kw_only=True)
class DomainEvent:
    source: object = field(default="default", repr=False, compare=False)
    event_id: UUID = field(default_factory=uuid4, init=False)
    occurred_on_utc: datetime = field(default_factory=lambda: datetime.now(timezone.utc), init=False)
