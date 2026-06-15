import pytest
from main import app
from fastapi.testclient import TestClient
import models
import os

@pytest.fixture
def client():
    if os.path.exists("test_badges.db"):
        os.remove("test_badges.db")

    os.environ["DATABASE_PATH"] = "test_badges.db"
    models.init_db("test_badges.db")

    with TestClient(app) as client:
        yield client

    if os.path.exists("test_badges.db"):
        os.remove("test_badges.db")

def test_gamification_badges(client):
    # Register & Login
    client.post("/api/register", json={"username": "badge_user", "password": "password"})
    client.post("/api/login", json={"username": "badge_user", "password": "password"})

    # Check initial badges
    res = client.get("/api/me")
    assert res.status_code == 200
    assert len(res.json()["badges"]) == 0

    # Complete 1 goal to earn "First Step"
    client.post("/api/goals", json={"description": "Goal 1"})
    client.post("/api/goals/1/complete")

    res = client.get("/api/me")
    badges = res.json()["badges"]
    assert len(badges) == 1
    assert badges[0]["name"] == "First Step"

    # Complete 4 more goals to earn "On a Roll"
    for i in range(2, 6):
        client.post("/api/goals", json={"description": f"Goal {i}"})
        client.post(f"/api/goals/{i}/complete")

    res = client.get("/api/me")
    badges = res.json()["badges"]
    assert len(badges) == 2
    assert any(b["name"] == "On a Roll" for b in badges)
