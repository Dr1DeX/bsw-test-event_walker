import json
from typing import Union

import aio_pika

from app.bets.schema import EventActionsSchema
from app.infrastructure.broker import get_broker_connection


async def publish_event_to_queue(queue_name: str, message: list[dict]):
    connection = await get_broker_connection()
    channel = await connection.channel()
    message_body = json.dumps(message).encode()
    await channel.default_exchange.publish(
        aio_pika.Message(body=message_body),
        routing_key=queue_name
    )
