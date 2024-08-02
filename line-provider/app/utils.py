import json
from typing import Union

import aio_pika

from app.event.schema import EventSchema
from app.infrastructure.broker import get_broker_connection


async def publish_event_to_queue(queue_name: str, message: Union[EventSchema, list[EventSchema]]):
    connection = await get_broker_connection()
    channel = await connection.channel()

    if isinstance(message, list):
        message_body = json.dumps([event.dict() for event in message]).encode()
    else:
        message_body = message.json().encode()

    await channel.default_exchange.publish(
        aio_pika.Message(body=message_body),
        routing_key=queue_name
    )
