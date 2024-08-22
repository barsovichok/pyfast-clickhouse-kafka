from fastapi import HTTPException
from typing import Sequence, Type
from sqlalchemy import table, column

from .engine import engine
from sqlmodel import Session, select, func

from app.models.User import User, UserCreate, UserUpdate


def get_user(user_id: int) -> User | None:
    """Return user by ID from the database."""
    with Session(engine) as session:
        return session.get(User, user_id)


def get_users() -> Sequence[User] | None:
    """Return all users from the database."""
    with Session(engine) as session:
        return session.exec(select(User)).all()


def get_count_users() -> int:
    """Return count of users in the database."""
    with Session(engine) as session:
        users_column = table('user', column('id'))
        statement = select(func.count()).select_from(users_column)
        return session.execute(statement).scalar()


def create_user(creating_user: UserCreate) -> User:
    """Create new user. Returns created user."""
    with Session(engine) as session:
        cast_user = User(email=creating_user.email,
                         first_name=creating_user.first_name,
                         last_name=creating_user.last_name,
                         avatar=str(creating_user.avatar))
        session.add(cast_user)
        session.commit()
        session.refresh(cast_user)
        return cast_user


def delete_user(user_id: int) -> bool:
    """Delete user by ID. Returns True if successful, else False."""
    try:
        with Session(engine) as session:
            user = session.get(User, user_id)
            session.delete(user)
            session.commit()
            return True
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False


def update_user(user_id: int, user: UserUpdate) -> HTTPException | Type[User]:
    """Update user data. Returns 404 if user not found, else updated user."""
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        if not db_user:
            return HTTPException(status_code=404, detail="User not found")
        user_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user_data)
        if user.avatar is not None:
            db_user.avatar = str(db_user.avatar)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
