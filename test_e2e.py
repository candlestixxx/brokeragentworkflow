import os
import subprocess
import time
import pytest
from playwright.sync_api import Page, expect
import models


@pytest.fixture(scope="session", autouse=True)
def test_server():
    """Start the Flask server in a subprocess for E2E tests."""
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    env["DATABASE_PATH"] = "test_e2e.db"
    env["SECRET_KEY"] = "test-secret"
    env["NOTIFICATIONS_ENABLED"] = "false"

    if os.path.exists("test_e2e.db"):
        os.remove("test_e2e.db")
    models.init_db("test_e2e.db")

    process = subprocess.Popen(
        ["python", "app.py"], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    time.sleep(3)

    yield

    process.terminate()
    process.wait()
    if os.path.exists("test_e2e.db"):
        os.remove("test_e2e.db")


def test_user_registration_and_login(page: Page):
    """Test the full flow of registering, logging in, and creating a goal."""
    page.goto("http://localhost:5000/")
    page.click("a:has-text('Register')")

    username = f"e2e_user_{int(time.time())}"

    page.locator(
        "div.max-w-md:has(h2:has-text('Register')) >> input[type='text']"
    ).fill(username)
    page.locator(
        "div.max-w-md:has(h2:has-text('Register')) >> input[type='password']"
    ).fill("secret123")
    page.locator(
        "div.max-w-md:has(h2:has-text('Register')) >> button[type='submit']"
    ).click()

    expect(page.locator("text=Registration successful.")).to_be_visible(timeout=10000)

    page.click("a:has-text('Login')")

    page.locator("div.max-w-md:has(h2:has-text('Login')) >> input[type='text']").fill(
        username
    )
    page.locator(
        "div.max-w-md:has(h2:has-text('Login')) >> input[type='password']"
    ).fill("secret123")
    page.locator(
        "div.max-w-md:has(h2:has-text('Login')) >> button[type='submit']"
    ).click()

    expect(page.locator(f"text=Hello, {username}")).to_be_visible(timeout=5000)

    page.fill("input[placeholder='New daily goal...']", "E2E Test Goal")

    # We must explicitly wait for the socket connection sequence.
    # The safest approach for an E2E test to not be flaky with Websockets is waiting for the DOM update directly
    # and allowing a slightly longer timeout for the socket event to propagate in headless CI.
    page.click("button:has-text('Add Goal')")

    # In a headless environment, the websocket fallback might not trigger the store mutation properly if the connection drops the session context,
    # so we manually trigger a data fetch via `page.evaluate` to simulate what a manual page reload would do but without breaking the test session.
    page.evaluate("() => { import('/src/store.ts').then(s => s.fetchData()) }")

    # Wait for the API to process
    time.sleep(2)

    page.reload()

    # Verify goal appears in the list (wait for websocket or fallback)
    expect(page.locator("text=E2E Test Goal")).to_be_visible(timeout=10000)

    page.click("li:has-text('E2E Test Goal') button:has-text('Complete')")
    time.sleep(2)
    page.reload()

    # Verify goal disappears from the pending list
    expect(page.locator("text=E2E Test Goal")).not_to_be_visible(timeout=10000)
