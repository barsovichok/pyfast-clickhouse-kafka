
from pydantic import BaseModel


class AppStatus(BaseModel):
    """Class representing the status of the application."""
    database: bool
