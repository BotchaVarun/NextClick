"""Contact model - wraps the `contacts` collection (contact form submissions)."""
from datetime import datetime, timezone
from bson.objectid import ObjectId
from database.mongodb import get_db


class Contact:
    @staticmethod
    def _col():
        return get_db().contacts

    @staticmethod
    def create(data: dict):
        doc = {
            "name": data["name"].strip(),
            "email": data["email"].strip().lower(),
            "subject": data.get("subject", "General Inquiry").strip(),
            "message": data["message"].strip(),
            "is_read": False,
            "created_at": datetime.now(timezone.utc),
        }
        result = Contact._col().insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    @staticmethod
    def find_all(unread_only=False, page=1, per_page=15):
        query = {"is_read": False} if unread_only else {}
        skip = (page - 1) * per_page
        cursor = Contact._col().find(query).sort("created_at", -1).skip(skip).limit(per_page)
        total = Contact._col().count_documents(query)
        return list(cursor), total

    @staticmethod
    def find_by_id(contact_id):
        try:
            return Contact._col().find_one({"_id": ObjectId(contact_id)})
        except Exception:
            return None

    @staticmethod
    def mark_read(contact_id):
        Contact._col().update_one({"_id": ObjectId(contact_id)}, {"$set": {"is_read": True}})

    @staticmethod
    def delete(contact_id):
        Contact._col().delete_one({"_id": ObjectId(contact_id)})

    @staticmethod
    def unread_count():
        return Contact._col().count_documents({"is_read": False})
