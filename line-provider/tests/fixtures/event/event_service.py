import pytest_asyncio

from app.event.repository import EventRepository
from app.event.service import EventService


@pytest_asyncio.fixture
async def mock_event_service(fake_event_repository):
    return EventService(
        event_repository=fake_event_repository
    )


@pytest_asyncio.fixture
async def event_service(get_redis_connection, mock_event_service):
    return EventService(
        event_repository=EventRepository(redis_connection=get_redis_connection)
    )
