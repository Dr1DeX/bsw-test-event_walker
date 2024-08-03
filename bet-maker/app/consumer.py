from app.dependency import get_bets_service
from app.infrastructure.broker import get_broker_connection


async def make_broker_consumer():
    bets_service = await get_bets_service()
    connection = await get_broker_connection()
    channel = await connection.channel()
    queue = await channel.declare_queue('bet_queue', durable=True)
    await queue.consume(bets_service.consume_event)