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
    # Set public privacy manually in test DB to avoid JS execution flakiness over Websockets in headless environments
    user_id = models.create_user("public_e2e", "pass", "test_social.db")
    models.update_user_settings(user_id, True, True, "test_social.db")

    page.goto("http://localhost:5000/")
    page.click("a:has-text('Register')")
    username = f"public_user_{int(time.time())}"

    page.locator("div.max-w-md:has(h2:has-text('Register')) >> input[type='text']").fill(username)
    page.locator("div.max-w-md:has(h2:has-text('Register')) >> input[type='password']").fill("secret123")
    page.locator("div.max-w-md:has(h2:has-text('Register')) >> button[type='submit']").click()
    expect(page.locator("text=Registration successful.")).to_be_visible(timeout=5000)

    page.click("a:has-text('Login')")
    page.locator("div.max-w-md:has(h2:has-text('Login')) >> input[type='text']").fill(username)
    page.locator("div.max-w-md:has(h2:has-text('Login')) >> input[type='password']").fill("secret123")
    page.locator("div.max-w-md:has(h2:has-text('Login')) >> button[type='submit']").click()

    expect(page.locator(f"text=Hello, {username}")).to_be_visible(timeout=5000)

    # We click the community tab. The 'public_e2e' user generated in the test_server fixture will be present
    page.goto("http://localhost:5000/community")

    # Reload after navigation
    time.sleep(1)
    page.reload()

    expect(page.locator("text=Community Progress")).to_be_visible(timeout=5000)
