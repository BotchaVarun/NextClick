"""Business logic for the contact form workflow."""
from models.contact import Contact
from utils.validators import validate_contact_form
# Email notification is no longer sent automatically - enquiries are handed
# off via WhatsApp redirect instead (see routes/public/contact_routes.py).
# The import stays available if you want to re-enable email as a backup
# channel later: from utils.email_service import send_contact_notification


def submit_contact(form_data: dict):
    errors = validate_contact_form(form_data)
    if errors:
        return False, errors, None

    contact = Contact.create(form_data)
    return True, [], contact
