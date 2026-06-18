import pytest
from unittest.mock import patch
from tasks import trigger_morning_prompt, trigger_quarterly_reminder
import models

import os


@pytest.fixture(autouse=True)
def setup_database():
    """Setup a fresh test database before each test."""
    os.environ["DATABASE_PATH"] = "test_tasks.db"
    if os.path.exists("test_tasks.db"):
        os.remove("test_tasks.db")

    models.init_db("test_tasks.db")
    # Create test user for tasks (gets ID 1)
    models.create_user("task_user", "password123", "test_tasks.db")
    models.update_user_settings(1, True, False, "test_tasks.db")

    yield

    if os.path.exists("test_tasks.db"):
        os.remove("test_tasks.db")


@patch("tasks.notify_all")
def test_trigger_morning_prompt_no_goals(mock_notify_all):
    # No goals in DB, shouldn't send notification
    trigger_morning_prompt()
    mock_notify_all.assert_not_called()


@patch("tasks.notify_all")
def test_trigger_morning_prompt_with_goals(mock_notify_all):
    models.add_goal("Test daily goal", user_id=1)

    trigger_morning_prompt()
    mock_notify_all.assert_called_once()
    _, kwargs = mock_notify_all.call_args
    assert "Morning Goal Prompt" in kwargs["subject"]


@patch("tasks.notify_all")
def test_trigger_quarterly_reminder_no_initiatives(mock_notify_all):
    trigger_quarterly_reminder()
    mock_notify_all.assert_not_called()


@patch("tasks.notify_all")
def test_trigger_quarterly_reminder_with_initiatives(mock_notify_all):
    models.add_initiative("Q1", "Test quarterly initiative", user_id=1)

    trigger_quarterly_reminder()
    mock_notify_all.assert_called_once()
    _, kwargs = mock_notify_all.call_args
    assert "Quarterly Initiative" in kwargs["subject"]
