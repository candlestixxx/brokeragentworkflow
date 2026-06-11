import pytest
from playwright.sync_api import Page, expect
import time
import os
import subprocess
import models

@pytest.fixture(scope="session", autouse=True)
def test_server():
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    env["DATABASE_PATH"] = "test_social.db"
    env["SECRET_KEY"] = "test-secret"
    env["NOTIFICATIONS_ENABLED"] = "false"

    if os.path.exists("test_social.db"):
        os.remove("test_social.db")
    models.init_db("test_social.db")

    process = subprocess.Popen(
        ["python", "app.py"], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    time.sleep(3)
    yield
    process.terminate()
    process.wait()
    if os.path.exists("test_social.db"):
        os.remove("test_social.db")

def test_social_community_page(page: Page):
    page.goto("http://127.0.0.1:5000/")
    page.goto("http://127.0.0.1:5000/register")
    username = f"public_user_{int(time.time())}"

    page.locator("input[placeholder='Pick a handle']").fill(username)
    page.locator("input[placeholder='Make it strong']").fill("secret123")
    page.locator("button:has-text('Create Account')").click()
    expect(page.locator("text=Registration successful.")).to_be_visible(timeout=5000)

    page.goto("http://127.0.0.1:5000/login")
    page.locator("input[placeholder='Your handle']").fill(username)
    page.locator("input[placeholder='••••••••']").fill("secret123")
    page.locator("button:has-text('Sign In')").click()

    expect(page.locator("text=Dashboard")).to_be_visible(timeout=5000)

    page.goto("http://127.0.0.1:5000/settings")
    expect(page.locator("text=Privacy")).to_be_visible(timeout=5000)

    page.evaluate("() => { fetch('/api/me/settings', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ is_public: true }) }) }")
    time.sleep(1)

    page.goto("http://127.0.0.1:5000/community")
    time.sleep(2)
    page.reload()
    expect(page.locator("text=Shared Momentum")).to_be_visible(timeout=5000)

    expect(page.locator(f"text={username}").first).to_be_visible(timeout=5000)
