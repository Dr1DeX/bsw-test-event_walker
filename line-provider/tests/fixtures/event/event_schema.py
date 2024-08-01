from faker import Factory as FakerFactory

from app.event.schema import EventSchema

faker = FakerFactory.create()

FAKE_EVENT_ID = '123'


def mock_events() -> EventSchema:
    return EventSchema(
        event_id=faker.uuid4(),
        ratio=faker.random_digit(),
        deadline=faker.random_digit(),
        status=faker.name()
    )
