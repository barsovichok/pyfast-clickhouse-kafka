from http import HTTPStatus

import requests


def test_delete_method(app_url, default_user):
    """Test the DELETE method to delete a user."""
    user_id = default_user["id"]
    response = requests.delete(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_deleted_item_not_found(app_url, default_user):
    """Test the DELETE method to delete a user that does not exist."""
    user_id = default_user["id"]
    response = requests.delete(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NO_CONTENT
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND
