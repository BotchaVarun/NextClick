"""Service model - wraps the `services` collection (what the studio offers)."""
from datetime import datetime, timezone
from bson.objectid import ObjectId
from slugify import slugify
from database.mongodb import get_db


class Service:
    @staticmethod
    def _col():
        return get_db().services

    @staticmethod
    def create(data: dict):
        doc = {
            "title": data["title"].strip(),
            "slug": slugify(data["title"]),
            "short_description": data.get("short_description", "").strip(),
            "description": data.get("description", "").strip(),
            "icon": data.get("icon", "camera"),
            "image_url": data.get("image_url", ""),
            "order": int(data.get("order", 0)),
            "is_active": data.get("is_active", True),
            "created_at": datetime.now(timezone.utc),
        }
        result = Service._col().insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    @staticmethod
    def find_all(active_only=True):
        query = {"is_active": True} if active_only else {}
        return list(Service._col().find(query).sort("order", 1))

    @staticmethod
    def find_by_id(service_id):
        try:
            return Service._col().find_one({"_id": ObjectId(service_id)})
        except Exception:
            return None

    @staticmethod
    def find_by_slug(slug):
        return Service._col().find_one({"slug": slug, "is_active": True})

    @staticmethod
    def update(service_id, data: dict):
        updates = {k: v for k, v in data.items() if v is not None}
        if "title" in updates:
            updates["slug"] = slugify(updates["title"])
        Service._col().update_one({"_id": ObjectId(service_id)}, {"$set": updates})

    @staticmethod
    def delete(service_id):
        Service._col().delete_one({"_id": ObjectId(service_id)})
