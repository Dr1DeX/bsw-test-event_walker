import json
import aio_pika

from dataclasses import dataclass

from app.bets.repository.bet import BetsRepository
from app.bets.schema import EventsSchema, EventActionsSchema, BetsCreateSchema, BetsSchema
from app.utils import callback_eventer


@dataclass
class BetsService:
    bets_repository: BetsRepository

    async def consume_event(self, msg: aio_pika.abc.AbstractIncomingMessage):
        async with msg.process():
            event_body = json.loads(msg.body.decode())
            action = event_body.get('action')
            data = event_body.get('data')

            if action == 'update_status_event':
                await self.bets_repository.update_bet(event=data)

    @staticmethod
    async def get_events() -> list[EventsSchema]:
        action_message = EventActionsSchema(event_id='', action='get_events')
        events = await callback_eventer(action_message=action_message)

        return events

    @staticmethod
    async def get_event(event_id: str) -> EventsSchema:
        action_message = EventActionsSchema(event_id=event_id, action='get_event')
        event = await callback_eventer(action_message=action_message)
        return event

    async def get_bet(self, event_id: str) -> BetsSchema:
        bet = await self.bets_repository.get_bet(event_id=event_id)
        return BetsSchema.model_validate(bet)

    async def get_bets(self) -> list[BetsSchema]:
        bets = await self.bets_repository.get_bets()
        bets_schema = [BetsSchema.model_validate(bet) for bet in bets]
        return bets_schema

    async def create_bet(self, bet: BetsCreateSchema) -> BetsSchema:
        action_message = EventActionsSchema(event_id=bet.event_id, action='subscribe_event')
        subscribe_eventer = await callback_eventer(action_message=action_message)

        event_id = await self.bets_repository.create_bet(bet=bet, status=subscribe_eventer.status)
        created_event = await self.bets_repository.get_bet(event_id=event_id)

        bets_schema = BetsSchema(
            event_id=created_event.event_id,
            sum_bet=created_event.sum_bet,
            status=created_event.status
        )

        return bets_schema
