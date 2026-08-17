"""Pricing model - wraps the `pricing_packages` collection."""
from datetime import datetime, timezone
from bson.objectid import ObjectId
from database.mongodb import get_db


class Pricing:
    @staticmethod
    def _col():
        return get_db().pricing_packages

    @staticmethod
    def create(data: dict):
        doc = {
            "name": data["name"].strip(),
            "price": float(data["price"]),
            "duration": data.get("duration", ""),
            "features": data.get("features", []),
            "is_popular": data.get("is_popular", False),
            "order": int(data.get("order", 0)),
            "is_active": data.get("is_active", True),
            "created_at": datetime.now(timezone.utc),
        }
        result = Pricing._col().insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    @staticmethod
    def find_all(active_only=True):
        query = {"is_active": True} if active_only else {}
        return list(Pricing._col().find(query).sort("order", 1))

    @staticmethod
    def find_by_id(pkg_id):
        try:
            return Pricing._col().find_one({"_id": ObjectId(pkg_id)})
        except Exception:
            return None

    @staticmethod
    def update(pkg_id, data: dict):
        updates = {k: v for k, v in data.items() if v is not None}
        Pricing._col().update_one({"_id": ObjectId(pkg_id)}, {"$set": updates})

    @staticmethod
    def delete(pkg_id):
        Pricing._col().delete_one({"_id": ObjectId(pkg_id)})
