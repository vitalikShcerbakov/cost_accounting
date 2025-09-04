from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestAuth:
    token = None

    @classmethod
    def test_create_user(cls, test_client, user_payload):
        response = test_client.post("/api/auth/register", json=user_payload)
        response_json = response.json()
        assert response_json.get('email') == user_payload.get('email')
        assert response.status_code == status.HTTP_201_CREATED

    @classmethod
    def test_get_token(cls, test_client, user_payload):
        cls.test_create_user(test_client, user_payload)
        data = {
            "username": user_payload['name'],
            "password": user_payload['password'],
        }
        response = test_client.post("/api/auth/token", data=data)
        response_json = response.json()
        cls.token = response_json['access_token']
        assert len(cls.token) == 125
        assert response_json['token_type'] == "bearer"
        assert response.status_code == status.HTTP_200_OK

    @classmethod
    def test_get_me(cls, test_client, user_payload):
        cls.test_create_user(test_client, user_payload)
        headers = {"Authorization": f"Bearer {cls.token}"}
        response = test_client.get("/api/auth/me", headers=headers)
        assert response.status_code == status.HTTP_200_OK
