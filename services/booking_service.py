"""Business logic for the booking workflow: validation -> save -> notify."""
from models.booking import Booking
from utils.validators import validate_booking_form
from utils.email_service import send_booking_confirmation
# Admin notification now happens via WhatsApp redirect (see routes/public/
# booking_routes.py) instead of email. send_booking_confirmation still emails
# the CUSTOMER a "we received it" note - that's a different concern and stays.


def submit_booking(form_data: dict):
    """
    Returns (success: bool, errors: list[str], booking: dict|None)
    """
    errors = validate_booking_form(form_data)
    if errors:
        return False, errors, None

    booking = Booking.create(form_data)
    send_booking_confirmation(booking)
    return True, [], booking
