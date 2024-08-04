from app.event.repository import EventRepository
from app.event.service import EventService
from app.infrastructure.redis.accessor import get_redis_connection


async def get_event_repository(
) -> EventRepository:
    return EventRepository(redis_connection=await get_redis_connection())


async def get_event_service(
) -> EventService:
    return EventService(event_repository=await get_event_repository())
