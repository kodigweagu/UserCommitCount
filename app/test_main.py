import redis
from unittest import mock
from fastapi.testclient import TestClient
from main import app

r = redis.Redis(host='redis', port=6379)
client = TestClient(app)

def test_get_users():
    
    response = client.get("/users")
    assert response.status_code == 200

def test_get_most_frequent():
    response = client.get("/most-frequent")
    assert response.status_code == 200

@mock.patch('main.requests.get')
def test_error_users(mock_get):
    mock_get.return_value = mock.Mock()
    mock_get.return_value.status_code = 500
    r.flushall()

    response = client.get("/users")
    assert response.json() == None
    mock_get.assert_called_once()

@mock.patch('main.requests.get')
def test_error_most_frequent(mock_get):
    mock_get.return_value = mock.Mock()
    mock_get.return_value.status_code = 500
    r.flushall()

    response = client.get("/most-frequent")
    assert response.json() == None
    mock_get.assert_called_once()