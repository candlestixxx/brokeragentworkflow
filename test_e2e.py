import os
import subprocess
import time
import pytest
from playwright.sync_api import Page, expect
import models

@pytest.fixture(scope="session", autouse=True)
def test_server():
    """Start the Flask server in a subprocess for E2E tests."""
    # Start Flask
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    env["DATABASE_PATH"] = "test_e2e.db"
    env["SECRET_KEY"] = "test-secret"
    env["NOTIFICATIONS_ENABLED"] = "false"

    # Ensure fresh database
    if os.path.exists("test_e2e.db"):
        os.remove("test_e2e.db")
    models.init_db("test_e2e.db")

    process = subprocess.Popen(
        ["python", "app.py"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for server to be ready
    time.sleep(3)

    yield

    # Cleanup
    process.terminate()
    process.wait()
    if os.path.exists("test_e2e.db"):
        os.remove("test_e2e.db")

def test_user_registration_and_login(page: Page):
    """Test the full flow of registering, logging in, and creating a goal."""
    # 1. Register
    page.goto("http://localhost:5000/")

    # Toggle to register view
    page.click("a:has-text('Register')")

    # Add random string to avoid duplicate user issues between test runs
    import time
    username = f"e2e_user_{int(time.time())}"

    # Fill registration
    # Use robust locators targeting the labels within the view
    page.locator("div.max-w-md:has(h2:has-text('Register')) >> input[type='text']").fill(username)
    page.locator("div.max-w-md:has(h2:has-text('Register')) >> input[type='password']").fill("secret123")
    page.locator("div.max-w-md:has(h2:has-text('Register')) >> button[type='submit']").click()

    # Wait for success flash
    expect(page.locator("text=Registration successful.")).to_be_visible(timeout=5000)

    # Switch to login view
    page.click("a:has-text('Login')")

    # 2. Login
    page.locator("div.max-w-md:has(h2:has-text('Login')) >> input[type='text']").fill(username)
    page.locator("div.max-w-md:has(h2:has-text('Login')) >> input[type='password']").fill("secret123")
    page.locator("div.max-w-md:has(h2:has-text('Login')) >> button[type='submit']").click()

    # Wait for dashboard to load (username should be visible)
    expect(page.locator(f"text=Hello, {username}")).to_be_visible(timeout=5000)

    # 3. Add Goal
    page.fill("input[placeholder='New daily goal...']", "E2E Test Goal")
    page.click("button:has-text('Add Goal')")

    # Verify goal appears in the list
    expect(page.locator("text=E2E Test Goal")).to_be_visible()

    # 4. Complete Goal
    # Assuming there's a button next to the goal text
    page.click("li:has-text('E2E Test Goal') button:has-text('Complete')")

    # Verify goal disappears from the pending list
    expect(page.locator("text=E2E Test Goal")).not_to_be_visible(timeout=5000)
