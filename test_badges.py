import pytest
import os
from models import (
    init_db,
    get_user_badges,
    add_goal,
    complete_goal,
    add_habit,
    create_user,
)

DB_PATH = "test_badges.db"


@pytest.fixture(autouse=True)
def setup_teardown():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db(DB_PATH)
    yield
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


def test_no_badges():
    create_user("testuser", "pass", db_path=DB_PATH)
    badges = get_user_badges(1, db_path=DB_PATH)
    assert len(badges) == 0


def test_first_step_badge():
    create_user("testuser", "pass", db_path=DB_PATH)
    goal = add_goal("My Goal", user_id=1, db_path=DB_PATH)
    complete_goal(goal["id"], user_id=1, db_path=DB_PATH)

    badges = get_user_badges(1, db_path=DB_PATH)
    assert "First Step" in badges
    assert "Achiever" not in badges


def test_achiever_badge():
    create_user("testuser", "pass", db_path=DB_PATH)
    for i in range(10):
        goal = add_goal(f"Goal {i}", user_id=1, db_path=DB_PATH)
        complete_goal(goal["id"], user_id=1, db_path=DB_PATH)

    badges = get_user_badges(1, db_path=DB_PATH)
    assert "First Step" in badges
    assert "Achiever" in badges
    assert "Master" not in badges


def test_streak_badges():
    create_user("testuser", "pass", db_path=DB_PATH)
    habit_id = add_habit("Drink Water", user_id=1, db_path=DB_PATH)

    # We need to manipulate the streak directly for the test instead of simulating 7 days of API calls
    # as complete_habit enforces sequential dates

    # Let's import the Habit model to manipulate it
    from models import _get_session, Habit

    session = _get_session(DB_PATH)
    habit = session.get(Habit, habit_id)
    habit.highest_streak = 7
    session.commit()
    session.close()

    badges = get_user_badges(1, db_path=DB_PATH)
    assert "7-Day Streak" in badges
    assert "30-Day Streak" not in badges

    session = _get_session(DB_PATH)
    habit = session.get(Habit, habit_id)
    habit.highest_streak = 30
    session.commit()
    session.close()

    badges = get_user_badges(1, db_path=DB_PATH)
    assert "30-Day Streak" in badges
