import os

import dotenv
from sqlmodel import create_engine, SQLModel, text, Session, select

dotenv.load_dotenv()
engine = create_engine(url=os.getenv("DATABASE_ENGINE"), pool_size=int(os.getenv("DATABASE_POOL_SIZE")))


def create_db_and_tables():
    """Create database"""
    SQLModel.metadata.create_all(engine)


def check_availability() -> bool:
    """Check database availability"""
    try:
        with Session(engine) as session:
            session.exec(select(text("1")))
            return True
    except Exception as e:
        print(f"Database unavailable: {e}")
        return False
