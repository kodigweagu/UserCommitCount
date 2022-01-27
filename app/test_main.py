import requests_mock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200

def test_get_most_frequent():
    response = client.get("/most-frequent")
    assert response.status_code == 200

def test_error_users():
    with requests_mock.Mocker() as mock:
        mock.get('/users', status_code=500)
        response = client.get("/users")
        assert response.status_code == 500

def test_error_most_frequent():
    with requests_mock.Mocker() as mock:
        mock.get('/most-frequent', status_code=500)
        response = client.get("/most-frequent")
        assert response.status_code == 500