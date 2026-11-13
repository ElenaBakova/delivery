import json
from dataclasses import fields, is_dataclass
from datetime import date, datetime
from uuid import UUID

from fastapi.responses import JSONResponse

from libs.ddd import DomainEvent


def encode(value: object) -> object:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, UUID):
        return str(value)
    if is_dataclass(value) and not isinstance(value, type):
        return {
            field.name: getattr(value, field.name)
            for field in fields(value)
            if not (isinstance(value, DomainEvent) and field.name == "source")
        }
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


class ApplicationJSONResponse(JSONResponse):
    def render(self, content: object) -> bytes:
        return json.dumps(content, default=encode, ensure_ascii=False,
                          allow_nan=False, separators=(",", ":")).encode("utf-8")
