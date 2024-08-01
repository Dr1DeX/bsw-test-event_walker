from redis import asyncio as redis
from app.settings import Settings

settings = Settings()


async def get_redis_connection() -> redis:
    return redis.Redis(
        host=settings.CACHE_HOST,
        port=settings.CACHE_PORT,
        db=settings.CACHE_DB
    )
