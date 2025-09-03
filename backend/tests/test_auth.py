from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_healthy():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {'status': 'healthy'}


def test_create_user(test_client, user_payload):
    response = test_client.post("/api/auth/register", json=user_payload)
    response_json = response.json()
    assert response.status_code == 200


def test_get_token(test_client, user_payload_token):
    response = test_client.post("/api/auth/token", json=user_payload_token)
    response_json = response.json()
    print('response_json: ', response_json)
    assert response.status_code == 200
