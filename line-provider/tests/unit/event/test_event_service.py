import pytest

from app.event.schema import EventCreateSchema, EventSchema
from tests.fixtures.event.event_schema import FAKE_EVENT_ID

pytestmark = pytest.mark.asyncio


async def test_create_event__success(mock_event_service):
    event_data = EventCreateSchema(ratio=1.1, deadline=12345.0, status='unfinished')

    event = await mock_event_service.create_event(event=event_data)

    assert event.event_id == FAKE_EVENT_ID
    assert event.status == 'unfinished'
