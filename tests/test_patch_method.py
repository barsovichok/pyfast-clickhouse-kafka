from http import HTTPStatus

import requests

from app.models.User import User


def test_patch_method_changed_fields(app_url, default_user):
    """Test that patch method changed fields"""
    user_id = default_user["id"]
    get_response = requests.get(f"{app_url}/api/users/{user_id}")
    assert get_response.status_code == HTTPStatus.OK
    default_user["first_name"] = "ChangedFirstName"
    default_user["last_name"] = "ChangedLastName"
    default_user["email"] = "ChangedEmail@gmail.com"
    default_user["avatar"] = "https://changed.com/png/faces/updated1399-image.jpg"
    response = requests.patch(f"{app_url}/api/users/{user_id}", json=default_user)
    assert response.status_code == HTTPStatus.OK
    get_response = requests.get(f"{app_url}/api/users/{user_id}")
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json()["id"] == user_id
    response_json = response.json()
    User.model_validate(response_json)
    assert response_json["first_name"] == "ChangedFirstName"
    assert response_json["last_name"] == "ChangedLastName"
    assert response_json["email"] == "ChangedEmail@gmail.com"
    assert response_json["avatar"] == "https://changed.com/png/faces/updated1399-image.jpg"


def test_patch_method_update_only_first_name(app_url, default_user):
    """Check that patch method updates only first_name"""
    user_id = default_user["id"]
    default_user["first_name"] = "OnlyFirstName"
    default_user["avatar"] = "https://reqres.in/png/faces/updated1399-image.jpg"
    response = requests.patch(f"{app_url}/api/users/{user_id}", json=default_user)
    assert response.status_code == HTTPStatus.OK
    get_response = requests.get(f"{app_url}/api/users/{user_id}")
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json()["id"] == user_id
    assert get_response.json()["email"] == default_user["email"]
    assert get_response.json()["first_name"] == "OnlyFirstName"
    assert get_response.json()["last_name"] == default_user["last_name"]
    assert get_response.json()["avatar"] == default_user["avatar"]


def test_patch_method_update_only_last_name(app_url, default_user):
    """Check that patch method updates only last_name"""
    user_id = default_user["id"]
    default_user["last_name"] = "OnlyLastName"
    default_user["avatar"] = "https://reqres.in/png/faces/updated1399-image.jpg"
    response = requests.patch(f"{app_url}/api/users/{user_id}", json=default_user)
    assert response.status_code == HTTPStatus.OK
    get_response = requests.get(f"{app_url}/api/users/{user_id}")
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json()["id"] == user_id
    assert get_response.json()["email"] == default_user["email"]
    assert get_response.json()["first_name"] == default_user["first_name"]
    assert get_response.json()["last_name"] == "OnlyLastName"


def test_patch_method_update_only_email(app_url, default_user):
    """Check that patch method updates only email"""
    user_id = default_user["id"]
    default_user["email"] = "NewEmail@gmail.com"
    default_user["avatar"] = "https://reqres.in/png/faces/updated1399-image.jpg"
    response = requests.patch(f"{app_url}/api/users/{user_id}", json=default_user)
    assert response.status_code == HTTPStatus.OK
    get_response = requests.get(f"{app_url}/api/users/{user_id}")
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json()["id"] == user_id
    assert get_response.json()["email"] == "NewEmail@gmail.com"
    assert get_response.json()["first_name"] == default_user["first_name"]
    assert get_response.json()["last_name"] == default_user["last_name"]


def test_patch_method_update_only_avatar(app_url, default_user):
    """Check that patch method updates only avatar"""
    user_id = default_user["id"]
    default_user["avatar"] = "https://reqres.in/png/faces/updated1399-image.jpg"
    response = requests.patch(f"{app_url}/api/users/{user_id}", json=default_user)
    assert response.status_code == HTTPStatus.OK
    get_response = requests.get(f"{app_url}/api/users/{user_id}")
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json()["id"] == user_id
    assert get_response.json()["email"] == default_user["email"]
    assert get_response.json()["first_name"] == default_user["first_name"]
    assert get_response.json()["last_name"] == default_user["last_name"]
    assert get_response.json()["avatar"]


def test_patch_method_field_required(app_url, default_user):
    """Check that patch method returns 422 when required field is missing"""
    user_id = default_user["id"]
    del default_user["id"]
    response = requests.patch(f"{app_url}/api/users/{user_id}", json=default_user)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_patch_method_avatar_invalid(app_url, default_user):
    """Check that patch method returns 422 when avatar is invalid URL"""
    user_id = default_user["id"]
    default_user["avatar"] = "htteeepg"
    response = requests.patch(f"{app_url}/api/users/{user_id}", json=default_user)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_patch_method_email_invalid(app_url, default_user):
    """Check that patch method returns 422 when email is invalid format"""
    user_id = default_user["id"]
    default_user["email"] = "invalidemail"
    response = requests.patch(f"{app_url}/api/users/{user_id}", json=default_user)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_patch_method_not_found(app_url, default_user):
    """Check that patch method returns 404 when user not found"""
    deleted_user_id = default_user["id"]
    delete_response = requests.delete(f"{app_url}/api/users/{default_user["id"]}")
    assert delete_response.status_code == HTTPStatus.NO_CONTENT
    response = requests.patch(f"{app_url}/api/users/{deleted_user_id}, json={default_user}")
    assert response.status_code == HTTPStatus.NOT_FOUND
