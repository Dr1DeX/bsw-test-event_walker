import asyncio

import pytest

pytest_plugins = [
    "tests.fixtures.event.event_service",
    "tests.fixtures.event.event_repository",
    "tests.fixtures.event.event_schema",
    "tests.fixtures.infrastructure"
]


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
