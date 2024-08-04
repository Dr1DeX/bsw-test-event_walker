import datetime
import json
import uuid

from dataclasses import dataclass
from redis import asyncio as redis
from app.event.exception import EventNotFoundException
from app.event.schema import EventSchema, EventCreateSchema, EventUpdatedStatusSchema


@dataclass
class EventRepository:
    redis_connection: redis

    async def create_event(self, event: EventCreateSchema) -> str:
        event_schema = EventSchema(
            event_id=str(uuid.uuid4()),
            **event.dict(exclude_none=True)
        )
        key = event_schema.event_id

        async with self.redis_connection as conn:
            await conn.set(key, event_schema.model_dump_json())
        return key

    async def get_event(self, event_id: str) -> EventSchema:
        async with self.redis_connection as conn:
            event_data = await conn.get(event_id)
            if event_data:
                event_schema = EventSchema.model_validate(json.loads(event_data))
                print('call get_event')
                return event_schema
            else:
                raise EventNotFoundException

    async def subscribe_event(self, event_id: str, data: EventSchema) -> None:
        async with self.redis_connection as conn:
            await conn.select(1)
            event_schema = EventUpdatedStatusSchema(event_id=data.event_id, status=data.status)
            print('call subscribe_eventer')
            await conn.set(event_id, event_schema.json())

    async def update_subscribe_event(self, event: EventUpdatedStatusSchema) -> EventUpdatedStatusSchema:
        async with self.redis_connection as conn:
            await conn.select(1)
            event_data = await conn.get(event.event_id)
            if event_data:
                event_schema = EventUpdatedStatusSchema.model_validate(json.loads(event_data))
                updated_event = event_schema.copy(update=event.dict(exclude_none=True))
                await conn.set(event.event_id, updated_event.json())
                updated_event_status = EventUpdatedStatusSchema(
                    event_id=event.event_id,
                    status=event.status
                )
                return updated_event_status

    async def update_events(self, updated_status: EventSchema) -> EventUpdatedStatusSchema:
        async with self.redis_connection as conn:
            event_data = await conn.get(updated_status.event_id)
            if event_data:
                event_schema = EventSchema.model_validate(json.loads(event_data))
                updated_event = event_schema.copy(update=updated_status.dict(exclude_none=True))
                await conn.set(updated_status.event_id, updated_event.json())
                updated_event_status = EventUpdatedStatusSchema(
                    event_id=updated_status.event_id,
                    status=updated_status.status
                )
                return updated_event_status
            else:
                raise EventNotFoundException

    async def get_events(self) -> list[EventSchema]:
        async with self.redis_connection as conn:
            keys = await conn.keys('*')
            if keys:
                event_data = await conn.mget(keys)
                current_time = datetime.datetime.now().timestamp()
                events = [
                    EventSchema.model_validate(json.loads(data))
                    for data in event_data
                    if EventSchema.model_validate(json.loads(data)).deadline >= current_time
                ]
                return events
            return []
