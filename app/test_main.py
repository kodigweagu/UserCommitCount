from fastapi.testclient import TestClient
from main import app
import pytest

pytest_plugins = ["docker_compose"]

client = TestClient(app)

@pytest.fixture(scope="session")
def test_read_main():
    response = client.get("/users")
    assert response.status_code == 200
    response = client.get("/most-frequent")
    assert response.status_code == 200