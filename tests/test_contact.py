"""Tests for contact form validation logic."""
from utils.validators import validate_contact_form


def test_contact_missing_fields():
    errors = validate_contact_form({})
    assert len(errors) > 0


def test_contact_short_message():
    data = {"name": "Jane", "email": "jane@example.com", "message": "hi"}
    errors = validate_contact_form(data)
    assert any("at least 10 characters" in e for e in errors)


def test_contact_valid_data():
    data = {"name": "Jane", "email": "jane@example.com", "message": "I would love to book a session with you."}
    errors = validate_contact_form(data)
    assert errors == []
