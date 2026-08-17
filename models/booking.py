"""
Booking model - wraps the `bookings` collection.
Stored as plain dicts; this class centralizes all queries/mutations
so routes never touch pymongo directly.
"""
from datetime import datetime, timezone
from bson.objectid import ObjectId
from database.mongodb import get_db

VALID_STATUSES = ("pending", "confirmed", "completed", "cancelled")


class Booking:
    collection_name = "bookings"

    @staticmethod
    def _col():
        return get_db()[Booking.collection_name]

    @staticmethod
    def create(data: dict):
        doc = {
            "full_name": data["full_name"].strip(),
            "email": data["email"].strip().lower(),
            "phone": data.get("phone", "").strip(),
            "service_type": data.get("service_type", ""),
            "package": data.get("package", ""),
            "event_date": data.get("event_date"),      # stored as "YYYY-MM-DD" string
            "event_location": data.get("event_location", ""),
            "message": data.get("message", "").strip(),
            "status": "pending",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        result = Booking._col().insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    @staticmethod
    def find_all(status=None, page=1, per_page=15):
        query = {}
        if status and status != "all":
            query["status"] = status
        skip = (page - 1) * per_page
        cursor = Booking._col().find(query).sort("created_at", -1).skip(skip).limit(per_page)
        total = Booking._col().count_documents(query)
        return list(cursor), total

    @staticmethod
    def find_by_id(booking_id):
        try:
            return Booking._col().find_one({"_id": ObjectId(booking_id)})
        except Exception:
            return None

    @staticmethod
    def update_status(booking_id, status):
        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")
        Booking._col().update_one(
            {"_id": ObjectId(booking_id)},
            {"$set": {"status": status, "updated_at": datetime.now(timezone.utc)}},
        )

    @staticmethod
    def delete(booking_id):
        Booking._col().delete_one({"_id": ObjectId(booking_id)})

    @staticmethod
    def counts_by_status():
        pipeline = [{"$group": {"_id": "$status", "count": {"$sum": 1}}}]
        results = {row["_id"]: row["count"] for row in Booking._col().aggregate(pipeline)}
        return {s: results.get(s, 0) for s in VALID_STATUSES}
