from typing import Annotated

from fastapi import APIRouter, Depends

from app.event.dependency import get_event_service
from app.event.schema import EventSchema, EventCreateSchema
from app.event.service import EventService

router = APIRouter(prefix='/event', tags=['event'])


@router.post(
    '',
    response_model=EventSchema
)
async def create_event(
        event: EventSchema,
        event_service: Annotated[EventService, Depends(get_event_service)]
):
    return await event_service.create_event(event=event)


@router.put(
    '',
    response_model=EventSchema
)
async def update_event(
        event_id: str,
        updated_event: EventCreateSchema,
        event_service: Annotated[EventService, Depends(get_event_service)]
):
    return await event_service.update_event(event_id=event_id, update_data=updated_event)
