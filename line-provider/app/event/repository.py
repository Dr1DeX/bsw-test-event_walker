import datetime
import json
import uuid
from dataclasses import dataclass
from redis import asyncio as redis
from app.event.exception import EventNotFoundException
from app.event.schema import EventSchema, EventCreateSchema


@dataclass
class EventRepository:
    redis_connection: redis

    async def create_event(self, event: EventCreateSchema) -> str:
        event_schema = EventSchema(
            event_id=str(uuid.uuid4()),
            **event.dict(exclude_none=True)
        )
        key = event_schema.event_id

        async with self.redis_connection as redis:
            await redis.set(key, event_schema.model_dump_json())
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

    async def update_event(self, event_id, update_data: EventCreateSchema) -> EventSchema:
        async with self.redis_connection as redis:
            event_data = await redis.get(event_id)
            if event_data:
                event_schema = EventSchema.model_validate(json.loads(event_data))
                updated_event = event_schema.copy(update=update_data.dict(exclude_none=True))
                await self.redis_connection.set(event_id, updated_event.json())
                return updated_event
            else:
                raise EventNotFoundException

    async def get_events(self) -> list[EventSchema]:
        async with self.redis_connection as redis:
            keys = await redis.keys('*')
            if keys:
                event_data = await redis.mget(keys)
                events = [EventSchema.model_validate(json.loads(data)) for data in event_data]
                return events
            return []
