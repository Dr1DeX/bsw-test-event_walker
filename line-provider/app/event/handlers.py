from typing import Annotated

from fastapi import APIRouter, Depends

from app.event.dependency import get_event_service
from app.event.schema import EventSchema, EventCreateSchema, EventUpdatedStatusSchema
from app.event.service import EventService

router = APIRouter(prefix='/event', tags=['event'])


@router.post(
    '',
    response_model=EventSchema
)
async def create_event(
        event: EventCreateSchema,
        event_service: Annotated[EventService, Depends(get_event_service)]
):
    return await event_service.create_event(event=event)


@router.put(
    '',
    response_model=EventUpdatedStatusSchema
)
async def update_event_status(
        updated_status: EventSchema,
        event_service: Annotated[EventService, Depends(get_event_service)]
):
    return await event_service.update_events(updated_status=updated_status)
