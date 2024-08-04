import json

from dataclasses import dataclass

import aio_pika.abc

from app.event.repository import EventRepository
from app.event.schema import EventSchema, EventCreateSchema, EventMessageBody, EventUpdatedStatusSchema
from app.event.wrappers import handle_raisers
from app.utils import publish_event_to_queue, send_notification_callback


@dataclass
class EventService:
    event_repository: EventRepository

    @handle_raisers
    async def create_event(self, event: EventCreateSchema) -> EventSchema:
        event_id = await self.event_repository.create_event(event=event)
        event = await self.event_repository.get_event(event_id=event_id)

        return event

    @handle_raisers
    async def update_events(self, updated_status: EventSchema) -> EventUpdatedStatusSchema:

        event = await self.event_repository.update_events(updated_status=updated_status)
        subscribed_event = EventUpdatedStatusSchema(event_id=updated_status.event_id, status=updated_status.status)
        subscribe_event = await self.event_repository.update_subscribe_event(event=subscribed_event)
        await send_notification_callback(queue_name='bet_queue', message=subscribe_event, action='update_status_event')

        return event

    @handle_raisers
    async def get_event(self, event_id: str) -> EventSchema:
        return await self.event_repository.get_event(event_id=event_id)

    async def get_events(self) -> list[EventSchema]:
        return await self.event_repository.get_events()

    async def consume_event(self, message: aio_pika.abc.AbstractIncomingMessage):
        """Listen events to bet-maker service"""

        async with message.process():
            event_body = EventMessageBody(**json.loads(message.body.decode()))
            if event_body.action == 'get_event':
                event = await self.event_repository.get_event(event_id=event_body.event_id)
                await publish_event_to_queue(
                    queue_name=message.reply_to,
                    message=event,
                    correlation_id=message.correlation_id
                )
            if event_body.action == 'get_events':
                events = await self.event_repository.get_events()
                await publish_event_to_queue(
                    queue_name=message.reply_to,
                    message=events,
                    correlation_id=message.correlation_id
                )
            if event_body.action == 'subscribe_event':
                event = await self.event_repository.get_event(event_id=event_body.event_id)
                await self.event_repository.subscribe_event(event_id=event_body.event_id, data=event)
                await publish_event_to_queue(
                    queue_name=message.reply_to,
                    message=event,
                    correlation_id=message.correlation_id
                )