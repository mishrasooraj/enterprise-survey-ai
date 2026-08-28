from types import SimpleNamespace
from uuid import uuid4

import pytest

from app.events.event_consumer import IdempotentEventConsumer
from app.events.event_producer import InMemoryEventProducer
from app.events.event_schema import EventEnvelope
from app.events.event_schema import EventType


@pytest.mark.asyncio
async def test_in_memory_producer_records_events():
    producer = InMemoryEventProducer()
    event = EventEnvelope(
        event_type=EventType.survey_created,
        organization_id=uuid4(),
        idempotency_key="survey-created:1",
        payload={"survey_id": "1"},
    )
    await producer.publish(event)
    assert len(producer.events) == 1
    assert producer.events[0].event_type == EventType.survey_created


@pytest.mark.asyncio
async def test_idempotent_consumer_skips_duplicates():
    seen = []

    class TestConsumer(IdempotentEventConsumer):
        async def handle(self, event):
            seen.append(event.event_id)

    consumer = TestConsumer()
    event = EventEnvelope(
        event_type=EventType.document_uploaded,
        organization_id=uuid4(),
        idempotency_key="document-uploaded:1",
        payload={"document_id": "1"},
    )
    await consumer.consume(event)
    await consumer.consume(event)
    assert len(seen) == 1

