"""Smoke tests: public pages should return 200 and admin pages should redirect when logged out."""
import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize("path", [
    "/", "/about", "/services", "/pricing", "/testimonials",
    "/blog", "/contact", "/booking", "/faq", "/privacy-policy", "/terms",
])
def test_public_pages_load(client, path):
    response = client.get(path)
    assert response.status_code == 200


def test_404_page(client):
    response = client.get("/this-page-does-not-exist")
    assert response.status_code == 404


def test_admin_dashboard_requires_login(client):
    response = client.get("/admin/dashboard")
    assert response.status_code in (302, 401)  # redirected to login


def test_admin_login_page_loads(client):
    response = client.get("/admin/login")
    assert response.status_code == 200
