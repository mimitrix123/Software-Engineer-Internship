import os
os.environ["SECRET_KEY"] = "test-secret"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").status_code == 200


def test_register_login_and_post_crud():
    email = "pytest_user@example.com"
    register = client.post("/auth/register", json={"username": "pytest_user", "email": email, "password": "password123"})
    assert register.status_code in (201, 409)
    token = client.post("/auth/login", json={"username": "pytest_user", "email": email, "password": "password123"})
    assert token.status_code == 200
    headers = {"Authorization": f"Bearer {token.json()['access_token']}"}
    created = client.post("/posts", json={"title": "Test Post", "content": "Hello"}, headers=headers)
    assert created.status_code == 201
    post_id = created.json()["id"]
    assert client.get(f"/posts/{post_id}").status_code == 200
    assert client.put(f"/posts/{post_id}", json={"title": "Updated", "content": "Changed"}, headers=headers).status_code == 200
    assert client.post(f"/posts/{post_id}/like", headers=headers).status_code == 200
    comment = client.post(f"/posts/{post_id}/comments", json={"content": "Nice post"}, headers=headers)
    assert comment.status_code == 201
    assert client.get("/posts", params={"search": "Updated", "page": 1, "size": 10}).status_code == 200
    assert client.delete(f"/posts/{post_id}", headers=headers).status_code == 204


def test_validation_rejects_short_password():
    response = client.post("/auth/register", json={"username": "abc", "email": "bad@example.com", "password": "short"})
    assert response.status_code == 422
