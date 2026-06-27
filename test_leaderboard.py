from models import create_user, add_goal
from routers.social import get_leaderboard


def test_get_leaderboard(tmp_path):
    import os

    os.environ["DATABASE_PATH"] = str(tmp_path / "test.db")
    import models

    models.init_db()

    u1_id = create_user("u1", "p1")
    u2_id = create_user("u2", "p2")
    models.update_user_settings(user_id=u1_id, is_public=True)
    models.update_user_settings(user_id=u2_id, is_public=True)

    g1 = add_goal(description="g1", user_id=u1_id)
    models.complete_goal(g1["id"])

    # Provide mock dictionary matching what FastAPI deps return
    leaderboard = get_leaderboard(user={"id": u1_id, "username": "u1"})
    assert len(leaderboard) == 2
    assert leaderboard[0]["id"] == u1_id
    assert leaderboard[0]["score"] == 1
    assert leaderboard[1]["id"] == u2_id
    assert leaderboard[1]["score"] == 0
