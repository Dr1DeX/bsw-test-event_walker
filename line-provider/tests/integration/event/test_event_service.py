import pytest

from app.event.schema import EventSchema
from app.event.service import EventService

from tests.fixtures.event.event_schema import FAKE_EVENT_ID, mock_events

pytestmark = pytest.mark.asyncio


async def test_get_event__success(event_service: EventService, get_redis_connection):
    event = mock_events()
    event.event_id = FAKE_EVENT_ID

    conn = get_redis_connection
    await conn.set(event.event_id, event.json())
    event_data = await event_service.get_event(event_id=event.event_id)

    assert event_data.event_id == FAKE_EVENT_ID
    assert isinstance(event_data, EventSchema)
