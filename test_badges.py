import pytest
from app import app
import models
import json
import os

@pytest.fixture
def client():
    app.config["TESTING"] = True
    if os.path.exists("test_badges.db"):
        os.remove("test_badges.db")
    models.init_db("test_badges.db")

    with app.test_client() as client:
        os.environ["DATABASE_PATH"] = "test_badges.db"
        yield client

    if os.path.exists("test_badges.db"):
        os.remove("test_badges.db")

def test_gamification_badges(client):
    # Register & Login
    client.post("/api/register", data=json.dumps({"username": "badge_user", "password": "password"}), content_type="application/json")
    client.post("/api/login", data=json.dumps({"username": "badge_user", "password": "password"}), content_type="application/json")

    # Check initial badges
    res = client.get("/api/me")
    assert res.status_code == 200
    assert len(res.get_json()["badges"]) == 0

    # Complete 1 goal to earn "First Step"
    client.post("/api/goals", data=json.dumps({"description": "Goal 1"}), content_type="application/json")
    client.post("/api/goals/1/complete")

    res = client.get("/api/me")
    badges = res.get_json()["badges"]
    assert len(badges) == 1
    assert badges[0]["name"] == "First Step"

    # Complete 4 more goals to earn "On a Roll"
    for i in range(2, 6):
        client.post("/api/goals", data=json.dumps({"description": f"Goal {i}"}), content_type="application/json")
        client.post(f"/api/goals/{i}/complete")

    res = client.get("/api/me")
    badges = res.get_json()["badges"]
    assert len(badges) == 2
    assert any(b["name"] == "On a Roll" for b in badges)
