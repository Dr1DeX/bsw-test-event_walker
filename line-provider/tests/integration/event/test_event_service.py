import pytest

from app.event.schema import EventSchema, EventCreateSchema
from app.event.service import EventService

from tests.fixtures.event.event_schema import FAKE_EVENT_ID, mock_events

pytestmark = pytest.mark.asyncio


async def test_get_event__success(event_service: EventService, get_redis_connection):
    event = mock_events()
    event.event_id = FAKE_EVENT_ID
    conn = await get_redis_connection

    await conn.set(event.event_id, event.json())
    event_data = await event_service.get_event(event_id=event.event_id)

    assert event_data.event_id == FAKE_EVENT_ID
    assert isinstance(event_data, EventSchema)


async def test_get_events__success(event_service: EventService):
    events_data = await event_service.get_events()

    assert 6 == len(events_data)


async def test_update_event__success(event_service: EventService, get_redis_connection):
    event = EventCreateSchema(status='sample')
    event_mock = mock_events()
    event_mock.event_id = FAKE_EVENT_ID
    conn = await get_redis_connection

    await conn.set(event_mock.event_id, event_mock.json())
    event_data = await event_service.update_event(event_id=FAKE_EVENT_ID, update_data=event)

    assert event_data.event_id == FAKE_EVENT_ID
    assert event_data.status == event.status
    assert isinstance(event_data, EventSchema)
