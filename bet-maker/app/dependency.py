from app.bets.repository import BetsRepository
from app.bets.service import BetsService
from app.infrastructure.database.accessor import AsyncSessionFactory


async def get_bets_repository(
) -> BetsRepository:
    return BetsRepository(db_session=AsyncSessionFactory())


async def get_bets_service(
) -> BetsService:
    return BetsService(
        bets_repository=await get_bets_repository(),  # Depends не дергатеться
    )
