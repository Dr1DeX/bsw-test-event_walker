from dataclasses import dataclass

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.bets.models import Bets
from app.bets.schema import BetsCreateSchema, EventUpdatedStatusSchema


@dataclass
class BetsRepository:
    db_session: AsyncSession

    async def create_bet(self, bet: BetsCreateSchema, status: str) -> str:
        query = insert(Bets).values(
            status=status,
            **bet.dict(exclude_none=True)).returning(Bets.event_id)

        async with self.db_session as session:
            event_id: str = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            return event_id

    async def get_bets(self) -> list[Bets]:
        async with self.db_session as session:
            return (await session.execute(select(Bets))).scalars().all()

    async def get_bet(self, event_id: str) -> Bets:
        query = select(Bets).where(Bets.event_id == event_id)
        async with self.db_session as session:
            bet = (await session.execute(query)).scalar_one_or_none()
            return bet

    async def update_bet(self, event: dict) -> None:
        updated_event = EventUpdatedStatusSchema(status=event.get('status'))
        event_id = event.get('event_id')
        query = (
            update(Bets)
            .where(Bets.event_id == event_id)
            .values(**updated_event.dict(exclude_none=True))
        )

        async with self.db_session as session:
            await session.execute(query)
            await session.commit()
