import json
from dataclasses import dataclass

import aio_pika.abc

from app.bets.repository.bet import BetsRepository
from app.bets.schema import EventsSchema, EventActionsSchema
from app.infrastructure.broker import get_broker_connection


@dataclass
class BetsService:
    bets_repository: BetsRepository

    async def consume_event(self, message: aio_pika.abc.AbstractIncomingMessage):
        async with message.process():
            event_body = json.loads(message.body.decode())
            print(event_body)

            # if action_message.action == 'get_events':
            #     events = await self.get_events()
            #     await publish_event_to_queue(queue_name=message.reply_to, message=[event.dict() for event in events])

    async def get_events(self) -> list[EventsSchema]:
        connection = await get_broker_connection()
        channel = await connection.channel()

        response_queue = await channel.declare_queue(name='all_events_queue', durable=True)

        action_message = EventActionsSchema(event_id='', action='get_events')

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(action_message.dict()).encode(),
                reply_to=response_queue.name
            ),
            routing_key='event_queue'
        )

        incoming_message = await response_queue.get(timeout=30)
        event_data = json.loads(incoming_message.body.decode())
        events = [EventsSchema(**event) for event in event_data]

        return events
