"""Tests for the admin login flow."""
import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client


def test_login_page_renders(client):
    response = client.get("/admin/login")
    assert response.status_code == 200
    assert b"Log In" in response.data


def test_login_with_bad_credentials(client):
    response = client.post("/admin/login", data={
        "email": "nonexistent@example.com",
        "password": "wrongpassword",
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid email or password" in response.data
