import os
import pytest
from unittest.mock import patch
import models
from scheduler import trigger_morning_prompt, trigger_quarterly_reminder

@pytest.fixture(autouse=True)
def setup_teardown():
    # Disable actual notifications
    os.environ["NOTIFICATIONS_ENABLED"] = "false"

    # Setup test DB
    os.environ["DATABASE_PATH"] = "test_scheduler.db"
    if os.path.exists("test_scheduler.db"):
        os.remove("test_scheduler.db")
    models.init_db("test_scheduler.db")

    yield

    # Teardown
    if os.path.exists("test_scheduler.db"):
        os.remove("test_scheduler.db")

@patch('scheduler.notify_all')
def test_morning_prompt_empty(mock_notify):
    trigger_morning_prompt()
    mock_notify.assert_not_called()

@patch('scheduler.notify_all')
def test_morning_prompt_with_goals(mock_notify):
    models.add_goal("Write tests")
    trigger_morning_prompt()
    mock_notify.assert_called_once()
    args, kwargs = mock_notify.call_args
    assert "1 pending One-Minute goals" in kwargs['body']

@patch('scheduler.notify_all')
def test_quarterly_reminder_empty(mock_notify):
    trigger_quarterly_reminder()
    mock_notify.assert_not_called()

@patch('scheduler.notify_all')
def test_quarterly_reminder_with_initiatives(mock_notify):
    models.add_initiative("Q1", "Launch Dashboard")
    trigger_quarterly_reminder()
    mock_notify.assert_called_once()
    args, kwargs = mock_notify.call_args
    assert "1 pending quarterly initiatives" in kwargs['body']
