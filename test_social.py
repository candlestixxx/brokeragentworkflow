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
        ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "5000"], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    time.sleep(3)
    yield
    process.terminate()
    process.wait()
    if os.path.exists("test_social.db"):
        os.remove("test_social.db")

def test_social_community_page(page: Page):
    page.goto("http://127.0.0.1:5000/login")
    page.goto("http://127.0.0.1:5000/register")
    username = f"public_user_{int(time.time())}"

    page.locator("div.max-w-md:has(h2:has-text('Join FocusOS')) >> input[type='text']").fill(username)
    page.locator("div.max-w-md:has(h2:has-text('Join FocusOS')) >> input[type='password']").fill("secret123")
    page.locator("div.max-w-md:has(h2:has-text('Join FocusOS')) >> button[type='submit']").click()


    page.goto("http://127.0.0.1:5000/login")
    page.locator("div.max-w-md:has(h2:has-text('Welcome Back')) >> input[type='text']").fill(username)
    page.locator("div.max-w-md:has(h2:has-text('Welcome Back')) >> input[type='password']").fill("secret123")
    page.locator("div.max-w-md:has(h2:has-text('Welcome Back')) >> button[type='submit']").click()



    page.goto("http://127.0.0.1:5000/settings")
    page.wait_for_load_state("networkidle")



    page.evaluate("() => { fetch('/api/me/settings', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ is_public: true }) }) }")
    time.sleep(1)

    page.goto("http://127.0.0.1:5000/community")
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    page.reload()


