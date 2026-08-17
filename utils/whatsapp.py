"""
Builds WhatsApp "click-to-chat" links (wa.me) so form submissions can hand off
directly to a WhatsApp conversation with the business owner, instead of email.

No WhatsApp Business API, no Meta developer account, no approval process needed -
this uses WhatsApp's public click-to-chat URL scheme, which just opens a chat
with a pre-filled message. The visitor still has to tap "Send" on the WhatsApp
side (WhatsApp doesn't allow sites to send messages without the user's
confirmation) - but this happens instantly after form submit, and requires no
setup cost.
"""
from urllib.parse import quote


def normalize_whatsapp_number(raw_number: str) -> str:
    """Strip everything except digits. wa.me expects country code + number,
    no +, no spaces, no dashes. e.g. '+91 98765 43210' -> '919876543210'."""
    return "".join(ch for ch in (raw_number or "") if ch.isdigit())


def build_whatsapp_link(business_number: str, message: str) -> str | None:
    """Returns a wa.me link that opens WhatsApp with `message` pre-filled,
    addressed to `business_number`. Returns None if no number is configured,
    so callers can fall back gracefully (e.g. just show the saved-to-dashboard
    confirmation instead of trying to redirect anywhere)."""
    number = normalize_whatsapp_number(business_number)
    if not number:
        return None
    return f"https://wa.me/{number}?text={quote(message)}"


def contact_enquiry_message(form_data: dict) -> str:
    """Formats a contact form submission into a readable WhatsApp message."""
    return (
        "New enquiry from the website:\n\n"
        f"Name: {form_data.get('name', '')}\n"
        f"Email: {form_data.get('email', '')}\n"
        f"Subject: {form_data.get('subject', 'General Inquiry')}\n"
        f"Message: {form_data.get('message', '')}"
    )


def booking_enquiry_message(form_data: dict) -> str:
    """Formats a booking form submission into a readable WhatsApp message."""
    return (
        "New booking enquiry from the website:\n\n"
        f"Name: {form_data.get('full_name', '')}\n"
        f"Email: {form_data.get('email', '')}\n"
        f"Phone: {form_data.get('phone', '')}\n"
        f"Service: {form_data.get('service_type', '')}\n"
        f"Package: {form_data.get('package', '')}\n"
        f"Event Date: {form_data.get('event_date', '')}\n"
        f"Location: {form_data.get('event_location', '')}\n"
        f"Message: {form_data.get('message', '')}"
    )
