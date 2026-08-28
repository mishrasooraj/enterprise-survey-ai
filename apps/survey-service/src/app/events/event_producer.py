from __future__ import annotations

import json
from abc import ABC
from abc import abstractmethod
from typing import Any

from app.events.event_logging import logger
from app.events.event_schema import EventEnvelope


class EventProducer(ABC):
    @abstractmethod
    async def publish(self, event: EventEnvelope) -> None:
        raise NotImplementedError


class InMemoryEventProducer(EventProducer):
    def __init__(self):
        self.events: list[EventEnvelope] = []

    async def publish(self, event: EventEnvelope) -> None:
        self.events.append(event)
        logger.info(
            "event_published",
            extra={"event": event.model_dump(mode="json")},
        )


class KafkaEventProducer(EventProducer):
    def __init__(self, client: Any, topic_prefix: str = "survey-service"):
        self.client = client
        self.topic_prefix = topic_prefix

    async def publish(self, event: EventEnvelope) -> None:
        topic = f"{self.topic_prefix}.{event.event_type}"
        payload = event.model_dump(mode="json")
        message = json.dumps(payload).encode("utf-8")
        try:
            if hasattr(self.client, "send_and_wait"):
                await self.client.send_and_wait(topic, message)
            elif hasattr(self.client, "publish"):
                await self.client.publish(topic, message)
            else:
                raise RuntimeError("Unsupported Kafka client.")
            logger.info("event_published", extra={"topic": topic, "event_id": str(event.event_id)})
        except Exception as exc:
            logger.exception("event_publish_failed", extra={"topic": topic, "event_id": str(event.event_id)})
            raise


class KafkaProducerFactory:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers

    def create(self) -> Any:
        try:
            from aiokafka import AIOKafkaProducer
        except Exception as exc:  # pragma: no cover - optional dependency guard
            raise RuntimeError("aiokafka is not installed.") from exc
        return AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)

