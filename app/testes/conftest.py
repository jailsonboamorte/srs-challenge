import pytest
from main import api
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def client_headers():
    token = None
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    with TestClient(api, headers=headers) as client:
        yield client
