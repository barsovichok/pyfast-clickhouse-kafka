from http import HTTPStatus

from fastapi import APIRouter

from app.database.postgres.engine import check_availability
from app.models.AppStatus import AppStatus

router = APIRouter()


@router.get("/status", status_code=HTTPStatus.OK)
def check_status() -> AppStatus:
    """Check the status of the application. Return database connection status """
    return AppStatus(database=check_availability())
