import os
from http import HTTPStatus
import json
import dotenv
import pytest
import requests

from app.models.User import User
from app.routers.users import get_count_users


@pytest.fixture(autouse=True, scope="session")
def env():
    """Returns environment variables"""
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def app_url():
    """Returns application URL from environment variables."""
    return os.getenv('APP_URL')


@pytest.fixture(scope="module")
def total_users() -> int:
    """Returns the total number of users in the database."""
    return get_count_users()


@pytest.fixture(scope="module")
def json_payloads(app_url):
    """Returns test data payloads from a JSON file."""
    with open("users.json") as f:
        test_data_payloads = json.load(f)
        return test_data_payloads


@pytest.fixture(scope="module")
def fill_test_data(app_url, json_payloads):
    """Creates users in the database and returns their IDs.
    After all tests, deletes the created users."""
    api_users = []
    for user in json_payloads:
        response = requests.post(f"{app_url}/api/users/", json=user)
        api_users.append(response.json())

    user_ids = [user["id"] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        response = requests.delete(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.fixture()
def users(app_url):
    """Returns users from the database via route /api/users."""
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.OK
    users = response.json().get("items")
    for user in users:
        User.model_validate(user)
    return users


@pytest.fixture()
def default_user(app_url, json_payloads):
    """Returns default user from a JSON file."""
    response = requests.post(f"{app_url}/api/users/", json=json_payloads[0])
    assert response.status_code == HTTPStatus.CREATED
    User.model_validate(response.json())
    return response.json()


@pytest.fixture()
def pagination(total_users, size):
    """Returns the number of pages for pagination."""
    if total_users % size == 0:
        return total_users // size
    else:
        return total_users // size + 1
