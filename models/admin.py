"""
Admin model - wraps the `admins` collection.
Implements Flask-Login's UserMixin interface.
"""
from datetime import datetime, timezone
from bson.objectid import ObjectId
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database.mongodb import get_db


class Admin(UserMixin):
    def __init__(self, doc):
        self._doc = doc

    # --- Flask-Login required property ---
    def get_id(self):
        return str(self._doc["_id"])

    @property
    def name(self):
        return self._doc.get("name")

    @property
    def email(self):
        return self._doc.get("email")

    @property
    def role(self):
        return self._doc.get("role", "admin")

    def check_password(self, password):
        return check_password_hash(self._doc["password_hash"], password)

    # --- Queries ---
    @staticmethod
    def find_by_email(email):
        doc = get_db().admins.find_one({"email": email.lower().strip()})
        return Admin(doc) if doc else None

    @staticmethod
    def find_by_id(admin_id):
        try:
            doc = get_db().admins.find_one({"_id": ObjectId(admin_id)})
        except Exception:
            return None
        return Admin(doc) if doc else None

    @staticmethod
    def create(name, email, password, role="admin"):
        db = get_db()
        doc = {
            "name": name,
            "email": email.lower().strip(),
            "password_hash": generate_password_hash(password),
            "role": role,
            "created_at": datetime.now(timezone.utc),
            "last_login": None,
        }
        result = db.admins.insert_one(doc)
        doc["_id"] = result.inserted_id
        return Admin(doc)

    def update_password(self, new_password):
        get_db().admins.update_one(
            {"_id": self._doc["_id"]},
            {"$set": {"password_hash": generate_password_hash(new_password)}},
        )

    def update_profile(self, name=None, email=None):
        updates = {}
        if name:
            updates["name"] = name
        if email:
            updates["email"] = email.lower().strip()
        if updates:
            get_db().admins.update_one({"_id": self._doc["_id"]}, {"$set": updates})

    def record_login(self):
        get_db().admins.update_one(
            {"_id": self._doc["_id"]},
            {"$set": {"last_login": datetime.now(timezone.utc)}},
        )
