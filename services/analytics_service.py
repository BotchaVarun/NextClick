"""
Business logic for the admin analytics dashboard.
Aggregates internal data (bookings/contacts/blog performance proxies);
actual traffic analytics come from GA4 embedded client-side (see analytics.html).
"""
from datetime import datetime, timedelta, timezone
from models.booking import Booking
from models.contact import Contact
from database.mongodb import get_db


def dashboard_summary():
    db = get_db()
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)

    return {
        "booking_counts": Booking.counts_by_status(),
        "total_bookings": db.bookings.count_documents({}),
        "recent_bookings": db.bookings.count_documents({"created_at": {"$gte": thirty_days_ago}}),
        "unread_contacts": Contact.unread_count(),
        "total_contacts": db.contacts.count_documents({}),
        "published_blogs": db.blogs.count_documents({"is_published": True}),
        "total_testimonials": db.testimonials.count_documents({}),
    }
