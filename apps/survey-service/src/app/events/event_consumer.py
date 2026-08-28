from __future__ import annotations

import json
from abc import ABC
from abc import abstractmethod
from collections.abc import Awaitable
from collections.abc import Callable
from typing import Any
from uuid import UUID

from app.events.event_logging import logger
from app.events.event_schema import EventEnvelope


class EventConsumer(ABC):
    @abstractmethod
    async def handle(self, event: EventEnvelope) -> None:
        raise NotImplementedError


class IdempotentEventConsumer(EventConsumer):
    def __init__(self):
        self.processed_event_ids: set[UUID] = set()

    async def consume(self, event: EventEnvelope) -> None:
        if event.event_id in self.processed_event_ids:
            logger.info("event_skipped", extra={"event_id": str(event.event_id), "reason": "duplicate"})
            return
        await self.handle(event)
        self.processed_event_ids.add(event.event_id)


class InMemoryEventConsumer(IdempotentEventConsumer):
    def __init__(self, handler: Callable[[EventEnvelope], Awaitable[None]]):
        super().__init__()
        self.handler = handler

    async def handle(self, event: EventEnvelope) -> None:
        await self.handler(event)


class KafkaEventConsumer(IdempotentEventConsumer):
    def __init__(self, client: Any, handler: Callable[[EventEnvelope], Awaitable[None]]):
        super().__init__()
        self.client = client
        self.handler = handler

    async def handle(self, event: EventEnvelope) -> None:
        await self.handler(event)

    async def process_message(self, raw_message: bytes) -> None:
        payload = json.loads(raw_message.decode("utf-8"))
        event = EventEnvelope.model_validate(payload)
        await self.consume(event)

