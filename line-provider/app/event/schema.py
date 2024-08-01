from typing import Optional

from pydantic import BaseModel


class EventSchema(BaseModel):
    ratio: float
    deadline: float
    status: str

    class Config:
        from_attributes = True


class EventUpdatedSchema(BaseModel):
    ratio: Optional[float] = None
    deadline: Optional[float] = None
    status: Optional[str] = None
