import pytest
from app import app
import models
import json

@pytest.fixture
def client():
    app.config["TESTING"] = True
    import os
    if os.path.exists("test_analytics.db"):
        os.remove("test_analytics.db")
    models.init_db("test_analytics.db")
    with app.test_client() as client:
        # Override the env var so models uses this db path automatically
        os.environ["DATABASE_PATH"] = "test_analytics.db"
        yield client

    if os.path.exists("test_analytics.db"):
        os.remove("test_analytics.db")

def test_analytics_api(client):
    # Register user
    res = client.post(
        "/api/register",
        data=json.dumps({"username": "analytics_user_2", "password": "password"}),
        content_type="application/json"
    )
    assert res.status_code == 201

    # Login
    client.post(
        "/api/login",
        data=json.dumps({"username": "analytics_user_2", "password": "password"}),
        content_type="application/json"
    )

    # Add goals
    res = client.post("/api/goals", data=json.dumps({"description": "Goal 1"}), content_type="application/json")
    assert res.status_code == 201
    res = client.post("/api/goals", data=json.dumps({"description": "Goal 2"}), content_type="application/json")

    # Complete one goal
    # Note: SQLite IDs start at 1 and auto-increment per table
    client.post("/api/goals/1/complete")

    # Check analytics
    res = client.get("/api/analytics")
    assert res.status_code == 200
    data = res.get_json()
    assert data["total_goals"] == 2
    assert data["completed_goals"] == 1
    assert data["pending_goals"] == 1
    assert data["completion_percentage"] == 50
    assert data["streak"] == 1
