import os
import pytest
from click.testing import CliRunner
from cli import cli
import models

# Use an in-memory database or a separate test DB
os.environ["DATABASE_PATH"] = "test_goals.db"


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(autouse=True)
def setup_teardown():
    # Disable notifications for tests to avoid hitting external APIs
    os.environ["NOTIFICATIONS_ENABLED"] = "false"

    # Setup
    if os.path.exists("test_goals.db"):
        os.remove("test_goals.db")

    # We must mock os.environ locally for the test DB
    os.environ["DATABASE_PATH"] = "test_goals.db"

    # Must explicitly pass the overridden DB_PATH
    models.init_db("test_goals.db")

    yield

    # Teardown
    if os.path.exists("test_goals.db"):
        os.remove("test_goals.db")


def test_add_goal(runner):
    result = runner.invoke(cli, ["add", "Write more tests"])
    assert result.exit_code == 0
    assert "Added goal: 'Write more tests'" in result.output


def test_list_goals(runner):
    # Empty first
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "No pending goals" in result.output

    # Add one and check
    runner.invoke(cli, ["add", "Write more tests"])
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "Pending One-Minute Goals" in result.output
    assert "Write more tests" in result.output


def test_complete_goal(runner):
    # Add a goal
    runner.invoke(cli, ["add", "Finish project"])

    # Complete the goal (which should be ID 1 in a fresh DB)
    result = runner.invoke(cli, ["complete", "1"])
    assert result.exit_code == 0
    assert "Goal 1 marked as completed" in result.output

    # Ensure it doesn't show up in list
    result = runner.invoke(cli, ["list"])
    assert "No pending goals" in result.output


def test_complete_invalid_goal(runner):
    result = runner.invoke(cli, ["complete", "999"])
    assert result.exit_code == 0
    assert "No goal found with ID 999" in result.output


def test_add_initiative(runner):
    result = runner.invoke(cli, ["add-initiative", "Q4", "Holiday Mailers"])
    assert result.exit_code == 0
    assert "Added quarterly initiative for Q4: 'Holiday Mailers'" in result.output


def test_list_initiatives(runner):
    # Empty first
    result = runner.invoke(cli, ["list-initiatives"])
    assert result.exit_code == 0
    assert "No pending initiatives" in result.output

    # Add one and check
    runner.invoke(cli, ["add-initiative", "Q4", "Holiday Mailers"])
    result = runner.invoke(cli, ["list-initiatives"])
    assert result.exit_code == 0
    assert "Pending Quarterly Initiatives" in result.output
    assert "Holiday Mailers" in result.output


def test_complete_initiative(runner):
    # Add an initiative
    runner.invoke(cli, ["add-initiative", "Q4", "Holiday Mailers"])

    # Complete the initiative (ID 1 in a fresh DB)
    result = runner.invoke(cli, ["complete-initiative", "1"])
    assert result.exit_code == 0
    assert "Initiative 1 marked as completed" in result.output

    # Ensure it doesn't show up in list
    result = runner.invoke(cli, ["list-initiatives"])
    assert "No pending initiatives" in result.output
