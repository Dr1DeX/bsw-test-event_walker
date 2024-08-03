from typing import Annotated

from fastapi import APIRouter, Depends

from app.bets.schema import EventsSchema
from app.bets.service import BetsService
from app.dependency import get_bets_service

router = APIRouter()


@router.get(
    '/events',
    response_model=list[EventsSchema]
)
async def get_events(
        bets_service: Annotated[BetsService, Depends(get_bets_service)]
):
    return await bets_service.get_events()
