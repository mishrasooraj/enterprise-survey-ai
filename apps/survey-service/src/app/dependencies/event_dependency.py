from app.events.event_producer import InMemoryEventProducer


_EVENT_PRODUCER = InMemoryEventProducer()


def get_event_producer():
    return _EVENT_PRODUCER

