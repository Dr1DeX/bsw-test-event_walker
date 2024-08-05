import json
import uuid
from typing import Union

import aio_pika

from app.bets.schema import EventActionsSchema, EventsSchema
from app.infrastructure.broker import get_broker_connection


async def callback_eventer(
        action_message: EventActionsSchema
) -> Union[list[EventsSchema], EventsSchema]:

    connection = await get_broker_connection()
    channel = await connection.channel()

    response_queue = await channel.declare_queue(
        '',
        exclusive=True,
        timeout=10
    )

    correlation_id = str(uuid.uuid4())
    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(action_message.dict()).encode(),
            reply_to=response_queue.name,
            correlation_id=correlation_id
        ),
        routing_key='event_queue'
    )

    incoming_message = None

    async with response_queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                if message.correlation_id == correlation_id:
                    incoming_message = message
                    break

    if incoming_message is None:
        raise Exception("No message received")

    event_data = json.loads(incoming_message.body.decode())

    if isinstance(event_data, list):
        await response_queue.delete()
        return [EventsSchema(**event) for event in event_data]
    await response_queue.delete()
    return EventsSchema(**event_data)
