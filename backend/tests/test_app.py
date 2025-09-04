from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_healthy():
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'healthy'}
