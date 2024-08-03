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
