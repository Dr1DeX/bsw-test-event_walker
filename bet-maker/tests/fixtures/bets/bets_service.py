import pytest_asyncio

from app.bets.repository import BetsRepository
from app.bets.service import BetsService


@pytest_asyncio.fixture
async def mock_bets_service(fake_bets_repository):
    return BetsService(bets_repository=fake_bets_repository)


@pytest_asyncio.fixture
async def bets_service(get_db_session, mock_bets_service):
    return BetsService(
        bets_repository=BetsRepository(db_session=get_db_session)
    )
