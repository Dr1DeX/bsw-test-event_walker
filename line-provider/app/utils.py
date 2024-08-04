import json
from typing import Union

import aio_pika

from app.event.schema import EventSchema, EventUpdatedStatusSchema
from app.infrastructure.broker import get_broker_connection


async def publish_event_to_queue(queue_name: str, correlation_id: str, message: Union[EventSchema, list[EventSchema]]):
    connection = await get_broker_connection()
    channel = await connection.channel()

    if isinstance(message, list):
        message_body = json.dumps([event.dict() for event in message]).encode()
    else:
        message_body = message.json().encode()

    await channel.default_exchange.publish(
        aio_pika.Message(body=message_body, correlation_id=correlation_id),
        routing_key=queue_name,
    )


async def send_notification_callback(
        queue_name: str,
        action: str,
        message: EventUpdatedStatusSchema
):
    connection = await get_broker_connection()
    channel = await connection.channel()

    message_body = json.dumps({
        'action': action,
        'data': message.dict()
    }).encode()

    await channel.default_exchange.publish(
        aio_pika.Message(body=message_body),
        routing_key=queue_name
    )
