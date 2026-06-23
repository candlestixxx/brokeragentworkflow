import pytest
from fastapi.testclient import TestClient
from main import app
import models
import os

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    os.environ["DATABASE_PATH"] = "test_social_api.db"
    if os.path.exists("test_social_api.db"):
        os.remove("test_social_api.db")
    models.init_db("test_social_api.db")

    # Create two users
    models.create_user("user1", "pass", "test_social_api.db")
    models.create_user("user2", "pass", "test_social_api.db")

    yield

    if os.path.exists("test_social_api.db"):
        os.remove("test_social_api.db")


def test_high_five_and_leaderboard():
    client.post("/api/login", json={"username": "user1", "password": "pass"})

    models.update_user_settings(1, is_public=True, db_path="test_social_api.db")

    # Add and complete goal for user1
    gid = models.add_goal("goal", user_id=1, db_path="test_social_api.db")["id"]
    models.complete_goal(gid, user_id=1, db_path="test_social_api.db")

    # Login as user 2 and high five
    client.post("/api/login", json={"username": "user2", "password": "pass"})
    res = client.post(f"/api/social/goals/{gid}/highfive")
    assert res.status_code == 200
    assert res.json()["message"] == "High-five sent!"

    # Test leaderboard
    res = client.get("/api/social/leaderboard")
    assert res.status_code == 200
    board = res.json()
    assert len(board) == 1
    assert board[0]["username"] == "user1"
    assert board[0]["completed_count"] == 1

    # Check if high five count appears in user 1 profile
    res = client.get("/api/social/users/1/profile")
    assert res.status_code == 200
    profile = res.json()
    assert profile["recent_completed_goals"][0]["high_fives"] == 1
