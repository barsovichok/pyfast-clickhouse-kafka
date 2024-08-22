from pydantic import BaseModel, EmailStr, HttpUrl
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """Class representing a user."""
    id: int | None = Field(primary_key=True, default=None)
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str


class UserCreate(BaseModel):
    """Class representing the data which user that can be created."""
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl


class UserUpdate(BaseModel):
    """Class representing the data which user that can be updated."""
    id: int
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    avatar: HttpUrl | None = None
