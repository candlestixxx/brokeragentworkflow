import pytest
from fastapi.testclient import TestClient
from main import app
import models
import os

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    os.environ["DATABASE_PATH"] = "test_ai_coach.db"
    if os.path.exists("test_ai_coach.db"):
        os.remove("test_ai_coach.db")
    models.init_db("test_ai_coach.db")
    models.create_user("user1", "pass", "test_ai_coach.db")
    yield
    if os.path.exists("test_ai_coach.db"):
        os.remove("test_ai_coach.db")


def test_ai_coach_suggest():
    client.post("/api/login", json={"username": "user1", "password": "pass"})

    response = client.post(
        "/api/coach/suggest", json={"goal_description": "start a fitness routine"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    assert len(data["suggestions"]) == 3
    assert "gym bag" in data["suggestions"][0].lower()


def test_ai_coach_empty():
    client.post("/api/login", json={"username": "user1", "password": "pass"})

    response = client.post("/api/coach/suggest", json={"goal_description": ""})
    assert response.status_code == 400


def test_ai_coach_insights_low_streak():
    client.post("/api/login", json={"username": "user1", "password": "pass"})
    response = client.post(
        "/api/coach/insights",
        json={"habit_description": "Drink Water", "current_streak": 2},
    )
    assert response.status_code == 200
    data = response.json()
    assert "insight" in data
    assert "getting started" in data["insight"].lower()


def test_ai_coach_insights_high_streak():
    client.post("/api/login", json={"username": "user1", "password": "pass"})
    response = client.post(
        "/api/coach/insights", json={"habit_description": "Read", "current_streak": 35}
    )
    assert response.status_code == 200
    data = response.json()
    assert "insight" in data
    assert "incredible streak" in data["insight"].lower()


def test_ai_coach_insights_empty():
    client.post("/api/login", json={"username": "user1", "password": "pass"})
    response = client.post(
        "/api/coach/insights", json={"habit_description": "", "current_streak": 5}
    )
    assert response.status_code == 400
