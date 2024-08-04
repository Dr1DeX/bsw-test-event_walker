from app.event.dependency import get_event_service
from app.infrastructure.broker import get_broker_connection


async def make_broker_connection():
    event_service = await get_event_service()
    connection = await get_broker_connection()
    channel = await connection.channel()
    queue = await channel.declare_queue('event_queue', durable=True)
    await queue.consume(event_service.consume_event)
