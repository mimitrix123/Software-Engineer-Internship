import os
os.environ["SECRET_KEY"] = "test-secret"
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_and_docs():
    assert client.get('/health').status_code == 200
    assert client.get('/docs').status_code == 200


def test_auth_and_project_lifecycle():
    email = 'week4@example.com'
    register = client.post('/auth/register', json={'email': email, 'password': 'password123'})
    assert register.status_code in (201, 409)
    login = client.post('/auth/login', json={'email': email, 'password': 'password123'})
    assert login.status_code == 200
    headers = {'Authorization': f"Bearer {login.json()['access_token']}"}
    created = client.post('/projects', headers=headers, json={'name': 'Lifecycle', 'description': 'Test'})
    assert created.status_code == 201
    pid = created.json()['id']
    assert client.get(f'/projects/{pid}', headers=headers).status_code == 200
    assert client.put(f'/projects/{pid}', headers=headers, json={'name': 'Updated', 'description': 'Changed'}).status_code == 200
    assert client.delete(f'/projects/{pid}', headers=headers).status_code == 204


def test_validation():
    response = client.post('/auth/register', json={'email': 'bad', 'password': 'short'})
    assert response.status_code == 422
