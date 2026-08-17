from flask import Blueprint, render_template
from middleware.auth_middleware import admin_required
from services.analytics_service import dashboard_summary
from models.booking import Booking
from models.contact import Contact

dashboard_bp = Blueprint("admin_dashboard", __name__)


@dashboard_bp.route("/dashboard")
@admin_required
def dashboard():
    summary = dashboard_summary()
    recent_bookings, _ = Booking.find_all(page=1, per_page=5)
    recent_contacts, _ = Contact.find_all(page=1, per_page=5)
    return render_template(
        "admin/dashboard.html",
        summary=summary,
        recent_bookings=recent_bookings,
        recent_contacts=recent_contacts,
    )
