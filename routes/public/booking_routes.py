from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.service import Service
from models.pricing import Pricing
from models.website_settings import WebsiteSettings
from services.booking_service import submit_booking
from middleware.security import rate_limit
from utils.seo import page_meta
from utils.whatsapp import build_whatsapp_link, booking_enquiry_message

booking_bp = Blueprint("booking", __name__)


@booking_bp.route("/booking", methods=["GET", "POST"])
def booking():
    settings = WebsiteSettings.get()
    if request.method == "POST":
        rate_limit("booking_form", max_requests=5, window_seconds=300)
        form_data = {
            "full_name": request.form.get("full_name", ""),
            "email": request.form.get("email", ""),
            "phone": request.form.get("phone", ""),
            "service_type": request.form.get("service_type", ""),
            "package": request.form.get("package", ""),
            "event_date": request.form.get("event_date", ""),
            "event_location": request.form.get("event_location", ""),
            "message": request.form.get("message", ""),
        }
        success, errors, _ = submit_booking(form_data)
        if success:
            whatsapp_link = build_whatsapp_link(
                settings.get("whatsapp_number"),
                booking_enquiry_message(form_data),
            )
            if whatsapp_link:
                # Booking is already saved to the DB (shows in Admin > Bookings)
                # and the customer already got a confirmation email; this just
                # hands the enquiry straight to your WhatsApp too.
                return redirect(whatsapp_link)
            flash("Your booking request has been received! We'll confirm availability within 24-48 hours.", "success")
            return redirect(url_for("booking.booking"))
        for error in errors:
            flash(error, "error")

    services = Service.find_all()
    packages = Pricing.find_all()
    meta = page_meta(title="Book a Session", description="Check availability and reserve your session date.")
    return render_template("public/booking.html", services=services, packages=packages, meta=meta)
