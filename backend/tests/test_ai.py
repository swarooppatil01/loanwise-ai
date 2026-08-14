from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_ai_requires_authentication():
    response = client.post(
        "/api/v1/ai/chat",
        json={
            "message": "Tell me about my financial profile."
        },
    )

    assert response.status_code in (401, 403)


def test_ai_empty_message_requires_authentication():
    response = client.post(
        "/api/v1/ai/chat",
        json={
            "message": "",
        },
    )

    assert response.status_code in (401, 403)


def test_ai_oversized_message_requires_authentication():
    response = client.post(
        "/api/v1/ai/chat",
        json={
            "message": "a" * 4001,
        },
    )

    assert response.status_code in (401, 403)
