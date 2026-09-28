import os
import pytest
from main import app
from fastapi.testclient import TestClient
import models


@pytest.fixture
def client():
    # Setup
    os.environ["DATABASE_PATH"] = "test_admin.db"

    if os.path.exists("test_admin.db"):
        os.remove("test_admin.db")

    models.init_db("test_admin.db")

    with TestClient(app) as client:
        yield client

    # Teardown
    if os.path.exists("test_admin.db"):
        os.remove("test_admin.db")


def login_test_user(client):
    models.create_user("admin_test_user", "password123")
    client.post("/api/login", json=dict(username="admin_test_user", password="password123"))


def test_api_admin_context_unauthenticated(client):
    rv = client.get("/api/admin/context")
    assert rv.status_code == 401


def test_api_admin_context_authenticated(client):
    login_test_user(client)
    rv = client.get("/api/admin/context")
    assert rv.status_code == 200

    data = rv.json()
    assert "memory" in data
    assert "vision" in data
    assert "roadmap" in data
    assert "todo" in data
    assert "changelog" in data
    assert "handoff" in data
