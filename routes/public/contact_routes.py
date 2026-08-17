from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.website_settings import WebsiteSettings
from services.contact_service import submit_contact
from middleware.security import rate_limit
from utils.seo import page_meta
from utils.whatsapp import build_whatsapp_link, contact_enquiry_message

contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/contact", methods=["GET", "POST"])
def contact():
    settings = WebsiteSettings.get()
    if request.method == "POST":
        rate_limit("contact_form", max_requests=5, window_seconds=300)
        form_data = {
            "name": request.form.get("name", ""),
            "email": request.form.get("email", ""),
            "subject": request.form.get("subject", ""),
            "message": request.form.get("message", ""),
        }
        success, errors, _ = submit_contact(form_data)
        if success:
            whatsapp_link = build_whatsapp_link(
                settings.get("whatsapp_number"),
                contact_enquiry_message(form_data),
            )
            if whatsapp_link:
                # Enquiry is already saved to the DB (shows in Admin > Contacts)
                # as a permanent record; this redirect just hands the visitor
                # straight into a WhatsApp chat with the details pre-filled.
                return redirect(whatsapp_link)
            flash("Thank you! Your message has been sent - we'll get back to you within 24 hours.", "success")
            return redirect(url_for("contact.contact"))
        for error in errors:
            flash(error, "error")

    meta = page_meta(title="Contact Us", description="Get in touch to discuss your photography needs.")
    return render_template("public/contact.html", settings=settings, meta=meta)
