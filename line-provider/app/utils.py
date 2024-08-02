import aio_pika

from app.infrastructure.broker import get_broker_connection


async def publish_event_to_queue(queue_name: str, message: str):
    connection = await get_broker_connection()
    channel = await connection.channel()
    await channel.default_exchange.publish(
        aio_pika.Message(body=message.encode()),
        routing_key=queue_name
    )
