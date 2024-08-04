import pytest

from app.bets.service import BetsService

pytest = pytest.mark.asyncio


async def test_get_events__success(mock_bets_service: BetsService):
    events = await mock_bets_service.get_events()

    assert len(events) == 5
    assert isinstance(events, list)
    assert events[0].status == 'sample'
    assert events[0].event_id == '123'
