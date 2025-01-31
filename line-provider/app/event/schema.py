from typing import Optional

from pydantic import BaseModel


class EventSchema(BaseModel):
    event_id: str
    ratio: float
    deadline: float
    status: str


class EventCreateSchema(BaseModel):
    ratio: Optional[float] = None
    deadline: Optional[float] = None
    status: Optional[str] = None


class EventUpdatedStatusSchema(BaseModel):
    event_id: str
    status: str


class EventMessageBody(BaseModel):
    event_id: str
    action: str
