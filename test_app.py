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

def login_test_user(client):
    # Setup test user
    models.create_user("testuser", "testpassword")
    client.post('/api/login', json=dict(username='testuser', password='testpassword'))

def test_spa_root(client):
    rv = client.get('/')
    assert rv.status_code == 200
    # Because we migrated to Vite, the root HTML is just an empty div#app shell.
    assert b'<div id="app"></div>' in rv.data

def test_api_goals_empty(client):
    login_test_user(client)
    rv = client.get('/api/goals')
    assert rv.status_code == 200
    assert rv.json == {"goals": []}

def test_api_add_goal(client):
    login_test_user(client)
    rv = client.post('/api/goals', json=dict(description='Test API Goal'))
    assert rv.status_code == 201
    assert rv.json['message'] == "Goal added."
    assert rv.json['id'] is not None

def test_api_complete_goal(client):
    login_test_user(client)
    models.add_goal("To be completed", user_id=1)
    rv = client.post('/api/goals/1/complete')
    assert rv.status_code == 200
    assert rv.json['message'] == "Goal 1 completed."

def test_api_add_initiative(client):
    login_test_user(client)
    rv = client.post('/api/initiatives', json=dict(quarter='Q1', description='Test Web Initiative'))
    assert rv.status_code == 201
    assert rv.json['message'] == "Initiative added."
    assert rv.json['id'] is not None

def test_api_complete_initiative(client):
    login_test_user(client)
    models.add_initiative("Q2", "Web Init", user_id=1)
    rv = client.post('/api/initiatives/1/complete')
    assert rv.status_code == 200
    assert rv.json['message'] == "Initiative 1 completed."
