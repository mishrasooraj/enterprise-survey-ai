from app.events.event_producer import InMemoryEventProducer


def get_event_producer() -> InMemoryEventProducer:
    return InMemoryEventProducer()

