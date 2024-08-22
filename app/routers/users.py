
from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate

from app.database.postgres import users
from app.kafka.Producer import send_event_to_kafka
from app.models.User import User, UserCreate, UserUpdate
from app.routers.data import metrics

router = APIRouter(prefix="/api/users")


@router.get("/count", status_code=HTTPStatus.OK)
def get_count_users() -> int:
    """Returns the number of users in the database"""
    return users.get_count_users()


@router.get("/", status_code=HTTPStatus.OK)
def get_users() -> Page[User]:
    """Returns a paginated list of users"""
    return paginate(users.get_users())


@router.get("/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    """Returns a single user by ID"""
    if user_id <= 0:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be a positive integer")
    user = users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user


@router.post("/", status_code=HTTPStatus.CREATED)
def create_user(user: UserCreate) -> User:
    """Creates a new user"""
    UserCreate.model_validate(user)
    created_user = users.create_user(user)
    """Sends data to the kafka server"""
    send_event_to_kafka("create_user", f"{created_user.model_dump()}")
    metrics()
    return created_user


@router.patch("/{user_id}", status_code=HTTPStatus.OK)
def update_user(user_id: int, user: UserUpdate):
    """Updates an existing user by ID"""
    if user_id <= 0:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be a positive integer")
    UserUpdate.model_validate(user.model_dump())
    return users.update_user(user_id, user)


@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int):
    """Deletes a user by ID"""
    if user_id <= 0:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be a positive integer")
    if not users.delete_user(user_id):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    users.delete_user(user_id)
    return {"message": "User deleted successfully"}


