import aio_pika

from app.settings import Settings


async def get_broker_connection() -> aio_pika.abc.AbstractConnection:
    settings = Settings()
    return await aio_pika.connect_robust(url=settings.BROKER_URL)
