"""
WebsiteSettings model - wraps the `website_settings` collection.
Stored as a small set of key/value documents (e.g. key="general", key="seo_defaults")
so different setting groups can be updated independently.
"""
from database.mongodb import get_db

DEFAULT_HERO_IMAGE = (
    "https://images.unsplash.com/photo-1520854221256-17451cc331bf"
    "?auto=format&fit=crop&w=1600&q=80"
)

DEFAULTS = {
    "site_name": "Your Brand Photography",
    "tagline": "Timeless Moments, Beautifully Captured",
    "phone": "",
    "whatsapp_number": "",
    "email": "",
    "hero_image": DEFAULT_HERO_IMAGE,
    "address": "",
    "instagram": "",
    "facebook": "",
    "pinterest": "",
    "primary_color": "#1C1C1E",
    "accent_color": "#C9A46A",
}


class WebsiteSettings:
    @staticmethod
    def _col():
        return get_db().website_settings

    @staticmethod
    def get(key="general"):
        doc = WebsiteSettings._col().find_one({"key": key})
        if not doc:
            return DEFAULTS.copy() if key == "general" else {}
        return doc.get("values", {})

    @staticmethod
    def update(key, values: dict):
        WebsiteSettings._col().update_one(
            {"key": key},
            {"$set": {"values": values}},
            upsert=True,
        )
