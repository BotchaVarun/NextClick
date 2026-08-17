"""Reusable form validation helpers used across public + admin routes."""
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^[\d\s()+\-]{7,20}$")


def is_valid_email(email: str) -> bool:
    return bool(email) and bool(EMAIL_RE.match(email.strip()))


def is_valid_phone(phone: str) -> bool:
    if not phone:
        return True  # phone is often optional
    return bool(PHONE_RE.match(phone.strip()))


def require_fields(data: dict, fields: list[str]) -> list[str]:
    """Returns a list of human-readable errors for any missing required fields."""
    errors = []
    for field in fields:
        value = data.get(field, "")
        if not value or not str(value).strip():
            label = field.replace("_", " ").title()
            errors.append(f"{label} is required.")
    return errors


def validate_contact_form(data: dict) -> list[str]:
    errors = require_fields(data, ["name", "email", "message"])
    if data.get("email") and not is_valid_email(data["email"]):
        errors.append("Please enter a valid email address.")
    if data.get("message") and len(data["message"].strip()) < 10:
        errors.append("Message must be at least 10 characters.")
    return errors


def validate_booking_form(data: dict) -> list[str]:
    errors = require_fields(data, ["full_name", "email", "event_date", "service_type"])
    if data.get("email") and not is_valid_email(data["email"]):
        errors.append("Please enter a valid email address.")
    if data.get("phone") and not is_valid_phone(data["phone"]):
        errors.append("Please enter a valid phone number.")
    return errors
