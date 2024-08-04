from typing import Annotated

from fastapi import APIRouter, Depends

from app.bets.schema import EventsSchema, BetsSchema, BetsCreateSchema
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


@router.get(
    '/event/{event_id}',
    response_model=EventsSchema
)
async def get_event(
        event_id: str,
        bets_service: Annotated[BetsService, Depends(get_bets_service)]
):
    return await bets_service.get_event(event_id=event_id)


@router.post(
    '/bet',
    response_model=BetsSchema
)
async def create_bet(
        bet: BetsCreateSchema,
        bets_service: Annotated[BetsService, Depends(get_bets_service)]

):
    return await bets_service.create_bet(bet=bet)


@router.get(
    '/bets',
    response_model=list[BetsSchema]
)
async def get_bets(
        bets_service: Annotated[BetsService, Depends(get_bets_service)]
):
    return await bets_service.get_bets()


@router.get(
    '/bet/{event_id}',
    response_model=BetsSchema
)
async def get_bet(
        event_id: str,
        bets_service: Annotated[BetsService, Depends(get_bets_service)]
):
    return await bets_service.get_bet(event_id=event_id)
