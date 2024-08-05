from faker import Factory as FakerFactory

from app.bets.schema import EventsSchema

faker = FakerFactory.create()


def mock_events() -> EventsSchema:
    return EventsSchema(
        event_id=faker.uuid4(),
        ratio=faker.random_digit(),
        deadline=faker.random_digit(),
        status=faker.name()
    )
