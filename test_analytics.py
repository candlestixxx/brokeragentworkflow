import pytest
from main import app
from fastapi.testclient import TestClient
import models
import os


@pytest.fixture
def client():
    if os.path.exists("test_analytics.db"):
        os.remove("test_analytics.db")

    os.environ["DATABASE_PATH"] = "test_analytics.db"
    models.init_db("test_analytics.db")

    with TestClient(app) as client:
        yield client

    if os.path.exists("test_analytics.db"):
        os.remove("test_analytics.db")


def test_analytics_api(client):
    # Register user
    res = client.post(
        "/api/register", json={"username": "analytics_user_2", "password": "password"}
    )
    assert res.status_code == 201

    # Login
    client.post(
        "/api/login", json={"username": "analytics_user_2", "password": "password"}
    )

    # Add goals
    res = client.post("/api/goals", json={"description": "Goal 1"})
    assert res.status_code == 201
    res = client.post("/api/goals", json={"description": "Goal 2"})

    # Complete one goal
    # Note: SQLite IDs start at 1 and auto-increment per table
    client.post("/api/goals/1/complete")

    # Check analytics
    res = client.get("/api/analytics")
    assert res.status_code == 200
    data = res.json()
    assert data["total_goals"] == 2
    assert data["completed_goals"] == 1
    assert data["pending_goals"] == 1
    assert data["completion_percentage"] == 50
    assert data["streak"] == 1
