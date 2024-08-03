from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.bets.repository import BetsRepository
from app.bets.service import BetsService
from app.infrastructure.database import get_db_session


async def get_bets_repository(
        db_session: AsyncSession = Depends(get_db_session)
) -> BetsRepository:
    return BetsRepository(db_session=db_session)


async def get_bets_service(
        bets_repository: BetsRepository = Depends(get_bets_repository)
) -> BetsService:
    return BetsService(
        bets_repository=bets_repository
    )
