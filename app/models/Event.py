from pydantic import BaseModel


class Event(BaseModel):
    event_type: str
    description: str
