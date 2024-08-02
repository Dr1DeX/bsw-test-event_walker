import json
from dataclasses import dataclass

import aio_pika.abc

from app.event.repository import EventRepository
from app.event.schema import EventSchema, EventCreateSchema, EventMessageBody
from app.event.wrappers import handle_raisers
from app.utils import publish_event_to_queue


@dataclass
class EventService:
    event_repository: EventRepository

    @handle_raisers
    async def create_event(self, event: EventCreateSchema) -> EventSchema:
        event_id = await self.event_repository.create_event(event=event)
        event = await self.event_repository.get_event(event_id=event_id)

        await publish_event_to_queue(queue_name='bet_queue', message=event)

        return event

    @handle_raisers
    async def update_event(self, event_id: str, update_data: EventCreateSchema) -> EventSchema:
        event = await self.event_repository.update_event(event_id=event_id, update_data=update_data)

        await publish_event_to_queue(queue_name='bet_queue', message=event)

        return event

    @handle_raisers
    async def get_event(self, event_id: str) -> EventSchema:
        return await self.event_repository.get_event(event_id=event_id)

    async def get_events(self) -> list[EventSchema]:
        return await self.event_repository.get_events()

    async def consume_event(self, message: aio_pika.abc.AbstractIncomingMessage):
        async with message.process():
            event_body = EventMessageBody(**json.loads(message.body.decode()))
            if event_body.action == 'get_event':
                event = await self.get_event(event_id=event_body.event_id)
                await publish_event_to_queue(queue_name='bet_queue', message=event)
            if event_body.action == 'get_events':
                events = await self.get_events()
                await publish_event_to_queue(queue_name='bet_queue', message=events)
