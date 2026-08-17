"""Tests for booking form validation logic."""
from utils.validators import validate_booking_form


def test_booking_missing_required_fields():
    errors = validate_booking_form({})
    assert len(errors) > 0
    assert any("Full Name" in e for e in errors)


def test_booking_invalid_email():
    data = {
        "full_name": "Jane Doe",
        "email": "not-an-email",
        "event_date": "2026-12-01",
        "service_type": "Wedding Photography",
    }
    errors = validate_booking_form(data)
    assert any("valid email" in e for e in errors)


def test_booking_valid_data():
    data = {
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "event_date": "2026-12-01",
        "service_type": "Wedding Photography",
        "phone": "+1 555 123 4567",
    }
    errors = validate_booking_form(data)
    assert errors == []
