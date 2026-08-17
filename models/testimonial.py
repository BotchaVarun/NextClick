"""Testimonial model - wraps the `testimonials` collection."""
from datetime import datetime, timezone
from bson.objectid import ObjectId
from database.mongodb import get_db


class Testimonial:
    @staticmethod
    def _col():
        return get_db().testimonials

    @staticmethod
    def create(data: dict):
        doc = {
            "client_name": data["client_name"].strip(),
            "event_type": data.get("event_type", "").strip(),
            "quote": data["quote"].strip(),
            "rating": int(data.get("rating", 5)),
            "photo_url": data.get("photo_url", ""),
            "is_featured": data.get("is_featured", False),
            "created_at": datetime.now(timezone.utc),
        }
        result = Testimonial._col().insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    @staticmethod
    def find_all(featured_only=False):
        query = {"is_featured": True} if featured_only else {}
        return list(Testimonial._col().find(query).sort("created_at", -1))

    @staticmethod
    def find_by_id(t_id):
        try:
            return Testimonial._col().find_one({"_id": ObjectId(t_id)})
        except Exception:
            return None

    @staticmethod
    def update(t_id, data: dict):
        updates = {k: v for k, v in data.items() if v is not None}
        Testimonial._col().update_one({"_id": ObjectId(t_id)}, {"$set": updates})

    @staticmethod
    def delete(t_id):
        Testimonial._col().delete_one({"_id": ObjectId(t_id)})
