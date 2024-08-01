from dataclasses import dataclass

from app.event.repository import EventRepository
from app.event.schema import EventSchema, EventCreateSchema
from app.event.wrappers import not_found_handle


@dataclass
class EventService:
    event_repository: EventRepository

    @not_found_handle
    async def create_event(self, event: EventSchema) -> EventSchema:
        event_id = await self.event_repository.create_event(event=event)
        return await self.event_repository.get_event(event_id=event_id)

    @not_found_handle
    async def update_event(self, event_id: str, update_data: EventCreateSchema) -> EventSchema:
        return await self.event_repository.update_event(event_id=event_id, update_data=update_data)

    @not_found_handle
    async def get_event(self, event_id: str) -> EventSchema:
        return await self.event_repository.get_event(event_id=event_id)
