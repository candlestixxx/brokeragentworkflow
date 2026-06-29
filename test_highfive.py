from models import create_user, add_goal, session_scope, HighFive


def test_add_highfive(tmp_path):
    import os

    os.environ["DATABASE_PATH"] = str(tmp_path / "test.db")
    import models

    models.init_db()

    u1_id = create_user("u1", "p1")
    u2_id = create_user("u2", "p2")
    g1 = add_goal(description="g1", user_id=u1_id)

    success = models.add_high_five(goal_id=g1["id"], sender_id=u2_id)
    assert success is True

    with session_scope() as session:
        hfs = session.query(HighFive).all()
        assert len(hfs) == 1
        assert hfs[0].sender_id == u2_id
        assert hfs[0].target_goal_id == g1["id"]
