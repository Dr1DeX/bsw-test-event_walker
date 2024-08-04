from typing import Optional

from pydantic import BaseModel


class EventsSchema(BaseModel):
    event_id: str
    ratio: float
    deadline: float
    status: str


class EventActionsSchema(BaseModel):
    event_id: Optional[str] = None
    action: str


class EventUpdatedStatusSchema(BaseModel):
    status: str


class BetsSchema(BaseModel):
    event_id: str
    sum_bet: float
    status: str

    class Config:
        from_attributes = True


class BetsCreateSchema(BaseModel):
    event_id: str
    sum_bet: float
