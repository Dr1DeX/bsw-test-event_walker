import datetime
import json
import uuid
from dataclasses import dataclass
from redis import asyncio as redis
from app.event.exception import EventNotFoundException
from app.event.schema import EventSchema, EventUpdatedSchema


@dataclass
class EventRepository:
    redis_connection: redis

    async def create_event(self, event: EventSchema) -> str:
        key = f'{uuid.uuid4()}'
        value = event.json()
        async with self.redis_connection as redis_conn:
            await redis_conn.set(key, value)
        return key

    async def get_event(self, event_id: str) -> EventSchema:
        async with self.redis_connection as redis:
            event_data = await redis.get(event_id)
            if event_data:
                event_schema = EventSchema.model_validate(json.loads(event_data))
                now_time = datetime.datetime.now().timestamp()
                if event_schema.deadline < now_time:
                    return event_schema
            else:
                raise EventNotFoundException

    async def update_event(self, event_id, update_data: EventUpdatedSchema) -> EventSchema:
        async with self.redis_connection as redis:
            event_data = await redis.get(event_id)
            if event_data:
                event_schema = EventSchema.model_validate(json.loads(event_data))
                updated_event = event_schema.copy(update=update_data.dict(exclude_none=True))
                await self.redis_connection.set(event_id, updated_event.json())
                return updated_event
            else:
                raise EventNotFoundException
