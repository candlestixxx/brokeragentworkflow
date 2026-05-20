import os
import pytest
from app import app
import models

@pytest.fixture
def client():
    # Setup
    os.environ["DATABASE_PATH"] = "test_app.db"
    # Disable actual notifications
    os.environ["NOTIFICATIONS_ENABLED"] = "false"

    if os.path.exists("test_app.db"):
        os.remove("test_app.db")

    models.init_db("test_app.db")

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

    # Teardown
    if os.path.exists("test_app.db"):
        os.remove("test_app.db")

def test_sms_reply_generic(client):
    rv = client.post('/sms', data=dict(Body='Hello'))
    assert b"Welcome to One-Minute Manager. Reply 'list' to see pending goals." in rv.data

def test_sms_reply_list_empty(client):
    rv = client.post('/sms', data=dict(Body='list'))
    assert b"No pending daily goals. Great job!" in rv.data

def test_voice_reply(client):
    rv = client.post('/voice')
    assert b"Hello. I am your One-Minute Manager. You are doing great today. Goodbye." in rv.data

def test_dashboard_empty(client):
    rv = client.get('/')
    assert b"No pending daily goals." in rv.data
    assert b"No pending quarterly initiatives." in rv.data

def test_dashboard_add_goal(client):
    # Add via POST
    rv = client.post('/goal/add', data=dict(description='Test Dashboard Goal'), follow_redirects=True)
    assert b"Added goal: &#39;Test Dashboard Goal&#39;" in rv.data
    assert b"Test Dashboard Goal" in rv.data

def test_dashboard_complete_goal(client):
    models.add_goal("To be completed")
    rv = client.post('/goal/complete/1', follow_redirects=True)
    assert b"Goal 1 marked as completed!" in rv.data
    assert b"To be completed" not in rv.data

def test_dashboard_add_initiative(client):
    rv = client.post('/initiative/add', data=dict(quarter='Q1', description='Test Web Initiative'), follow_redirects=True)
    assert b"Added quarterly initiative for Q1" in rv.data
    assert b"Test Web Initiative" in rv.data

def test_dashboard_complete_initiative(client):
    models.add_initiative("Q2", "Web Init")
    rv = client.post('/initiative/complete/1', follow_redirects=True)
    assert b"Initiative 1 marked as completed!" in rv.data
    assert b"Web Init" not in rv.data
