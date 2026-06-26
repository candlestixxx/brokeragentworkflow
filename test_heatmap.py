import pytest
from fastapi.testclient import TestClient
from main import app
import models
import os

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    os.environ["DATABASE_PATH"] = "test_heatmap.db"
    if os.path.exists("test_heatmap.db"):
        os.remove("test_heatmap.db")
    models.init_db("test_heatmap.db")
    models.create_user("user1", "pass", "test_heatmap.db")
    yield
    if os.path.exists("test_heatmap.db"):
        os.remove("test_heatmap.db")

def test_get_heatmap():
    client.post("/api/login", json={"username": "user1", "password": "pass"})

    # Complete 2 goals
    gid1 = models.add_goal("goal 1", user_id=1, db_path="test_heatmap.db")["id"]
    gid2 = models.add_goal("goal 2", user_id=1, db_path="test_heatmap.db")["id"]

    models.complete_goal(gid1, user_id=1, db_path="test_heatmap.db")
    models.complete_goal(gid2, user_id=1, db_path="test_heatmap.db")

    response = client.get("/api/me/heatmap")
    assert response.status_code == 200
    data = response.json()

    # We should have one date entry with count 2
    assert len(data) == 1
    assert data[0]["count"] == 2
