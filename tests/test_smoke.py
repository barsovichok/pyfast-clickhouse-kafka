import requests


def test_status(app_url):
    """Test status of a given app"""
    response = requests.get(f"{app_url}/status")
    assert response.status_code == 200
    data = response.json()
    assert data["database"] is True
