from dataclasses import dataclass

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.bets.models import Bets
from app.bets.schema import EventsSchema


@dataclass
class BetsRepository:
    db_session: AsyncSession

    async def save_events(self, events: list[EventsSchema]) -> None:
        event_idx = [event.event_id for event in events]
        events_dicts = [event.dict() for event in events]

        query = insert(Bets).values(events_dicts)