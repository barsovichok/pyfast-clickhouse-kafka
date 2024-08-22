import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import dotenv

from app.kafka.Consumer import start_consumer

dotenv.load_dotenv()
import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.database.postgres.engine import create_db_and_tables
from app.routers import status, users, data

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    """FastAPI lifespan hook."""
    logging.info("Pyfast in started")
    try:
        create_db_and_tables()
        start_consumer()
        application.get("database")
    except Exception as e:
        logging.error(f"Error during DB initialization: {e}")
        raise
    yield
    logging.info("Pyfast in stopped")


app = FastAPI(lifespan=lifespan)
app.include_router(status.router)
app.include_router(users.router)
app.include_router(data.router)

add_pagination(app)


if __name__ == "__main__":
    create_db_and_tables()
    start_consumer()
    """Create the database and tables and run the FastAPI server locally."""
    uvicorn.run(app, host="localhost", port=8000)
