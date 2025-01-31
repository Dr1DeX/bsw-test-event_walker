import pytest_asyncio

from redis import asyncio as redis

from tests.fixtures.event.event_schema import mock_events
from tests.fixtures.settings import Settings

settings = Settings()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def init_db(event_loop, get_redis_connection):
    async with get_redis_connection as conn:
        events = [mock_events() for _ in range(5)]
        for event in events:
            await conn.set(event.event_id, event.json())
    yield


@pytest_asyncio.fixture(scope='session')
async def get_redis_connection():
    conn = redis.Redis(
        host=settings.CACHE_HOST,
        port=settings.CACHE_PORT,
        db=settings.CACHE_DB
    )
    yield conn
    await conn.flushdb()
    await conn.close()
