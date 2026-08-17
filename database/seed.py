"""
Seed script - populates MongoDB with initial data:
an admin account, default website settings, and sample services/pricing.

Run with:  python -m database.seed
"""
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from werkzeug.security import generate_password_hash
from app import create_app
from database.mongodb import get_db


def seed():
    app = create_app()
    with app.app_context():
        db = get_db()

        # --- Admin account ---
        if not db.admins.find_one({"email": "admin@yourbrand.com"}):
            db.admins.insert_one({
                "name": "Studio Admin",
                "email": "admin@yourbrand.com",
                "password_hash": generate_password_hash("ChangeMe123!"),
                "role": "super_admin",
                "created_at": datetime.now(timezone.utc),
                "last_login": None,
            })
            print("Created default admin -> admin@yourbrand.com / ChangeMe123!  (change immediately)")

        # --- Website settings ---
        defaults = {
            "site_name": "The Next CLick Studios",
            "tagline": "Your Story. Our Next Click.",
            "phone": "+1 (555) 123-4567",
            "email": "hello@yourbrand.com",
            "address": "123 Studio Lane, Your City",
            "instagram": "https://instagram.com/yourbrand",
            "facebook": "https://facebook.com/yourbrand",
            "pinterest": "https://pinterest.com/yourbrand",
            "primary_color": "#1C1C1E",
            "accent_color": "#C9A46A",
        }
        if not db.website_settings.find_one({"key": "general"}):
            db.website_settings.insert_one({"key": "general", "values": defaults})
            print("Seeded website_settings")

        # --- Sample services ---
        if db.services.count_documents({}) == 0:
            db.services.insert_many([
                {
                    "title": "Wedding Photography",
                    "slug": "wedding-photography",
                    "short_description": "Full-day coverage capturing every emotion of your big day.",
                    "description": "From getting ready to the last dance, we document your wedding "
                                    "with a candid, editorial style that feels timeless rather than trendy.",
                    "icon": "camera",
                    "order": 1,
                    "is_active": True,
                },
                {
                    "title": "Portrait Sessions",
                    "slug": "portrait-sessions",
                    "short_description": "Individual, couple, and family portraits in studio or on location.",
                    "description": "Relaxed, guided sessions designed to produce portraits you'll "
                                    "actually want on your walls.",
                    "icon": "user",
                    "order": 2,
                    "is_active": True,
                },
                {
                    "title": "Event Coverage",
                    "slug": "event-coverage",
                    "short_description": "Corporate events, engagements, and private celebrations.",
                    "description": "Discreet, professional coverage that captures the atmosphere "
                                    "without getting in the way of it.",
                    "icon": "calendar",
                    "order": 3,
                    "is_active": True,
                },
            ])
            print("Seeded services")

        # --- Sample pricing packages ---
        if db.pricing_packages.count_documents({}) == 0:
            db.pricing_packages.insert_many([
                {
                    "name": "Essential",
                    "price": 799,
                    "duration": "3 hours",
                    "features": ["1 photographer", "150+ edited photos", "Online gallery", "Print release"],
                    "is_popular": False,
                    "order": 1,
                    "is_active": True,
                },
                {
                    "name": "Signature",
                    "price": 1499,
                    "duration": "6 hours",
                    "features": ["2 photographers", "400+ edited photos", "Online gallery",
                                 "Engagement session", "Print release"],
                    "is_popular": True,
                    "order": 2,
                    "is_active": True,
                },
                {
                    "name": "Luxury",
                    "price": 2999,
                    "duration": "Full day",
                    "features": ["2 photographers", "Unlimited photos", "Same-day preview",
                                 "Premium album", "Engagement session", "Print release"],
                    "is_popular": False,
                    "order": 3,
                    "is_active": True,
                },
            ])
            print("Seeded pricing_packages")

        print("Seeding complete.")


if __name__ == "__main__":
    seed()
