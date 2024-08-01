from redis import asyncio as redis
from fastapi import Depends

from app.event.repository import EventRepository
from app.event.service import EventService
from app.infrastructure.redis.accessor import get_redis_connection


async def get_event_repository(
        redis_connection: redis = Depends(get_redis_connection)
) -> EventRepository:
    return EventRepository(redis_connection=redis_connection)


async def get_event_service(
        event_repository: EventRepository = Depends(get_event_repository)
) -> EventService:
    return EventService(event_repository=event_repository)
