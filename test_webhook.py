import os
import pytest
from webhook import app
from cli import init_db

@pytest.fixture
def client():
    # Setup
    os.environ["DATABASE_PATH"] = "test_webhook.db"

    if os.path.exists("test_webhook.db"):
        os.remove("test_webhook.db")

    init_db("test_webhook.db")

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

    # Teardown
    if os.path.exists("test_webhook.db"):
        os.remove("test_webhook.db")

def test_sms_reply_generic(client):
    rv = client.post('/sms', data=dict(Body='Hello'))
    assert b"Welcome to One-Minute Manager. Reply 'list' to see pending goals." in rv.data

def test_sms_reply_list_empty(client):
    rv = client.post('/sms', data=dict(Body='list'))
    assert b"No pending daily goals. Great job!" in rv.data

def test_voice_reply(client):
    rv = client.post('/voice')
    assert b"Hello. I am your One-Minute Manager. You are doing great today. Goodbye." in rv.data
