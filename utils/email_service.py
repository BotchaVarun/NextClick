"""Flask-Mail wrapper - sends booking/contact notification emails."""
from flask import current_app, render_template
from flask_mail import Mail, Message

mail = Mail()


def init_mail(app):
    mail.init_app(app)


def send_booking_notification(booking: dict):
    """Notify the studio admin of a new booking request."""
    _send(
        subject=f"New Booking Request - {booking['full_name']}",
        recipients=[current_app.config["ADMIN_NOTIFY_EMAIL"]],
        body=(
            f"New booking request received:\n\n"
            f"Name: {booking['full_name']}\n"
            f"Email: {booking['email']}\n"
            f"Phone: {booking.get('phone', 'N/A')}\n"
            f"Service: {booking.get('service_type', 'N/A')}\n"
            f"Package: {booking.get('package', 'N/A')}\n"
            f"Event Date: {booking.get('event_date', 'N/A')}\n"
            f"Location: {booking.get('event_location', 'N/A')}\n"
            f"Message: {booking.get('message', '')}\n"
        ),
    )


def send_booking_confirmation(booking: dict):
    """Send the client a friendly confirmation their request was received."""
    _send(
        subject="We've received your booking request",
        recipients=[booking["email"]],
        body=(
            f"Hi {booking['full_name']},\n\n"
            f"Thank you for reaching out! We've received your booking request for "
            f"{booking.get('event_date', 'your event')} and will confirm availability "
            f"within 24-48 hours.\n\n"
            f"Warmly,\n{current_app.config['SITE_NAME']}"
        ),
    )


def send_contact_notification(contact: dict):
    _send(
        subject=f"New Contact Message - {contact.get('subject', 'General Inquiry')}",
        recipients=[current_app.config["ADMIN_NOTIFY_EMAIL"]],
        body=(
            f"New contact form submission:\n\n"
            f"Name: {contact['name']}\n"
            f"Email: {contact['email']}\n"
            f"Subject: {contact.get('subject', '')}\n"
            f"Message:\n{contact['message']}\n"
        ),
    )


def _send(subject, recipients, body):
    try:
        msg = Message(subject=subject, recipients=recipients, body=body)
        mail.send(msg)
    except Exception as e:
        # Never let an email failure break the user-facing request
        current_app.logger.error("Email send failed: %s", e)
