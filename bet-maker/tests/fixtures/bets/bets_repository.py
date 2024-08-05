from dataclasses import dataclass

import pytest

from app.bets.schema import EventsSchema
from tests.fixtures.bets.bets_schema import mock_events


@dataclass
class FakeBetsRepository:
    async def get_events(self) -> list[EventsSchema]:
        events = [mock_events() for _ in range(5)]
        event_schema = [EventsSchema.model_validate(event) for event in events]
        event_schema[0].event_id = '123'
        event_schema[0].status = 'sample'

        return event_schema


@pytest.fixture
def fake_bets_repository():
    return FakeBetsRepository()
