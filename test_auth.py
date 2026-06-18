import pytest
from fastapi.testclient import TestClient
from main import app
import models
import os

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    os.environ["DATABASE_PATH"] = "test_auth.db"
    if os.path.exists("test_auth.db"):
        os.remove("test_auth.db")
    models.init_db("test_auth.db")
    yield
    if os.path.exists("test_auth.db"):
        os.remove("test_auth.db")


def test_register_success():
    response = client.post(
        "/api/register", json={"username": "newuser", "password": "password123"}
    )
    assert response.status_code == 201
    assert response.json() == {"message": "Registration successful."}


def test_register_weak_password():
    response = client.post(
        "/api/register", json={"username": "newuser2", "password": "123"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Password must be at least 6 characters long."}


def test_login_success():
    client.post(
        "/api/register", json={"username": "loginuser", "password": "password123"}
    )
    response = client.post(
        "/api/login", json={"username": "loginuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Logged in successfully."}


def test_login_failure():
    response = client.post(
        "/api/login", json={"username": "baduser", "password": "badpassword"}
    )
    assert response.status_code == 401


def test_logout():
    # Register and login first
    client.post(
        "/api/register", json={"username": "logoutuser", "password": "password123"}
    )
    login_response = client.post(
        "/api/login", json={"username": "logoutuser", "password": "password123"}
    )

    assert login_response.status_code == 200

    # Extract the cookie
    cookies = login_response.cookies

    # Perform logout request using the cookies

    # Set the cookie directly on the client to avoid Starlette deprecation warning
    client.cookies.update(cookies)
    logout_response = client.post("/api/logout")

    assert logout_response.status_code == 200
    assert logout_response.json() == {"message": "Logged out successfully."}

    # In FastAPI TestClient, a deleted cookie often translates to setting it with max-age=0 or empty value.
    # The exact behavior depends on how the response deletes it.
    assert not logout_response.cookies.get("session")
