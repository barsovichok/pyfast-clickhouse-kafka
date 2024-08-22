from http import HTTPStatus

import pytest
import requests

from app.models.User import User


def test_get_user_method(app_url, fill_test_data):
    """Tests GET /api/users/{user_id} method"""
    for user_id in (fill_test_data[0], fill_test_data[-1]):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK
        User.model_validate(response.json())


def test_get_user_method_not_allowed(app_url):
    """Test 405 error for GET /api/users """
    response = requests.patch(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_get_method_non_existed_values(app_url, json_payloads):
    """Test 404 error for GET /api/users/{user_id} with non-existent user_id"""
    create_response = requests.post(f"{app_url}/api/users/", json=json_payloads[0]).json()
    user_id = create_response["id"]
    requests.delete(f"{app_url}/api/users/{user_id}")
    response = requests.get(f"{app_url}/api/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, "kssdf"])
def test_get_method_unprocessable_entity(app_url, user_id):
    """Test 422 error for GET /api/users/{user_id} with invalid user_id"""
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
