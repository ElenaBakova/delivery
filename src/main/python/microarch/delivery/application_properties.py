import os
import re
import sysconfig
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, cast

import yaml


def load_configuration() -> dict[str, Any]:
    path = Path(__file__).resolve().parents[3] / "resources" / "application.yml"
    if not path.is_file():
        path = Path(sysconfig.get_path("data")) / "share" / "delivery" / "application.yml"
    config: object = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError("Application configuration must be a mapping")

    def resolve(value: Any) -> Any:
        if isinstance(value, dict):
            mapping = cast(dict[str, Any], value)
            return {key.replace("-", "_"): resolve(item) for key, item in mapping.items()}
        if isinstance(value, str):
            return re.sub(
                r"\$\{([^:}]+):([^}]*)\}",
                lambda match: os.getenv(match[1], match[2]),
                value,
            )
        return value

    return cast(dict[str, Any], resolve(config))


@dataclass(frozen=True)
class ApplicationProperties:
    @dataclass(frozen=True)
    class Grpc:
        @dataclass
        class GeoService:
            host: str | None = None
            port: int = 0

        geo_service: "ApplicationProperties.Grpc.GeoService" = field(
            default_factory=lambda: ApplicationProperties.Grpc.GeoService()
        )

    @dataclass
    class Kafka:
        stocks_events_topic: str | None = None
        baskets_events_topic: str | None = None

    grpc: Grpc = field(default_factory=Grpc)
    kafka: Kafka = field(default_factory=Kafka)

    @classmethod
    def load(cls, config: dict[str, Any] | None = None) -> "ApplicationProperties":
        if config is None:
            config = load_configuration()
        app = config.get("app", {})
        geo = app.get("grpc", {}).get("geo_service", {})
        kafka = app.get("kafka", {})
        return cls(
            grpc=cls.Grpc(
                geo_service=cls.Grpc.GeoService(
                    host=geo.get("host"),
                    port=int(geo.get("port", 0)),
                )
            ),
            kafka=cls.Kafka(
                stocks_events_topic=kafka.get("stocks_events_topic"),
                baskets_events_topic=kafka.get("baskets_events_topic"),
            ),
        )
