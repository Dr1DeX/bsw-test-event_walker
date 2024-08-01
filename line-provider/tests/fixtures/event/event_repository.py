from dataclasses import dataclass

import pytest

from app.event.schema import EventSchema, EventCreateSchema
from tests.fixtures.event.event_schema import FAKE_EVENT_ID, mock_events


@dataclass
class FakeEventRepository:
    async def get_event(self, event_id: str) -> EventSchema:
        event = mock_events()
        event.status = 'unfinished'
        event.event_id = event_id
        return event

    async def create_event(self, event: EventCreateSchema) -> EventSchema:
        event_id = FAKE_EVENT_ID
        return event_id


@pytest.fixture
def fake_event_repository():
    return FakeEventRepository()
