""" 
The main test module in our simple web application
tests the endpoints available in main (/users and /most-frequent) for:
one succesful response (GitHub responds with 200)
one failed response where GitHub responds with a 500
"""
import redis
from unittest import mock
from fastapi.testclient import TestClient
from main import app

# get an instance of the redis service
redis_instance = redis.Redis(host='redis', port=6379)
client = TestClient(app)

# tests /users succesful response (GitHub responds with 200)
def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200

# tests /most-frequent for default parameters succesful response (GitHub responds with 200)
def test_get_most_frequent():
    response = client.get("/most-frequent")
    assert response.status_code == 200

# tests /users for default parameters failed response where GitHub responds with a 500
@mock.patch('main.requests.get')
def test_error_users(mock_get):
    mock_get.return_value = mock.Mock()
    mock_get.return_value.status_code = 500
    # clean data in redis for test
    redis_instance.flushall()

    response = client.get("/users")
    assert response.json() == None
    mock_get.assert_called_once()

# tests /most-frequent for default parameters failed response where GitHub responds with a 500
@mock.patch('main.requests.get')
def test_error_most_frequent(mock_get):
    mock_get.return_value = mock.Mock()
    mock_get.return_value.status_code = 500
    # clean data in redis for test
    redis_instance.flushall()

    response = client.get("/most-frequent")
    assert response.json() == None
    mock_get.assert_called_once()