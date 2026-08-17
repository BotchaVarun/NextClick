"""
Database adapter.

This project originally used MongoDB Atlas, but this adapter supports both:
- real MongoDB when configured
- Firestore when FIRESTORE_PROJECT_ID / GOOGLE_APPLICATION_CREDENTIALS are set
- an in-memory fallback for local development when neither is available

The rest of the app keeps using a Mongo-like collection API, so we do not need to
rewrite every model/service file to change the backend.
"""
import json
import os
import tempfile
import uuid
from datetime import datetime, timezone
from types import SimpleNamespace

import certifi
import mongomock
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError
from werkzeug.security import generate_password_hash

try:  # pragma: no cover
    import firebase_admin
    from firebase_admin import credentials, firestore
except Exception:  # pragma: no cover
    firebase_admin = None
    credentials = None
    firestore = None

_client = None
_db = None


class FirestoreCursor:
    def __init__(self, docs):
        self._docs = docs
        self._skip = 0
        self._limit = None

    def sort(self, field, direction=-1):
        self._docs = sorted(
            self._docs,
            key=lambda doc: doc.get(field, 0) if field in doc else 0,
            reverse=direction == -1,
        )
        return self

    def skip(self, n):
        self._skip = n
        return self

    def limit(self, n):
        self._limit = n
        return self

    def __iter__(self):
        docs = self._docs[self._skip:]
        if self._limit is not None:
            docs = docs[: self._limit]
        return iter(docs)


class FirestoreCollection:
    def __init__(self, database, name, client=None):
        self._database = database
        self._name = name
        self._client = client

    def _collection_ref(self):
        if self._client is None:
            return None
        return self._client.collection(self._name)

    def _docs(self):
        if self._client is not None:
            return [
                {**doc.to_dict(), "_id": str(doc.id)}
                for doc in self._collection_ref().stream()
            ]
        return list(self._database._memory_store.get(self._name, {}).values())

    def _match(self, doc, query):
        if not query:
            return True
        for key, value in query.items():
            if key == "_id":
                if isinstance(value, ObjectId):
                    value = str(value)
                if doc.get("_id") != value:
                    return False
                continue
            if isinstance(value, dict):
                for op, expected in value.items():
                    actual = doc.get(key)
                    if op == "$gte" and not (actual is not None and actual >= expected):
                        return False
                    if op == "$gt" and not (actual is not None and actual > expected):
                        return False
                    if op == "$lte" and not (actual is not None and actual <= expected):
                        return False
                    if op == "$lt" and not (actual is not None and actual < expected):
                        return False
                    if op == "$ne" and actual == expected:
                        return False
                    if op == "$in" and actual not in expected:
                        return False
                continue
            if doc.get(key) != value:
                return False
        return True

    def _extract_id(self, doc):
        return str(doc.get("_id") or ObjectId())

    def find_one(self, query=None):
        query = query or {}
        for doc in self._docs():
            if self._match(doc, query):
                return doc
        return None

    def find(self, query=None):
        query = query or {}
        matches = [doc for doc in self._docs() if self._match(doc, query)]
        return FirestoreCursor(matches)

    def insert_one(self, doc):
        if "_id" not in doc:
            doc["_id"] = str(ObjectId())
        if self._client is not None:
            self._collection_ref().document(str(doc["_id"])).set(doc)
            return SimpleNamespace(inserted_id=doc["_id"])
        self._database._memory_store.setdefault(self._name, {})[str(doc["_id"])] = doc
        return SimpleNamespace(inserted_id=doc["_id"])

    def insert_many(self, docs):
        inserted = []
        for doc in docs:
            result = self.insert_one(doc)
            inserted.append(result.inserted_id)
        return SimpleNamespace(inserted_ids=inserted)

    def update_one(self, query, update):
        if self._client is not None:
            ref = self.find_one(query)
            if not ref:
                return
            doc = ref
            changes = update.get("$set", {})
            for key, value in changes.items():
                doc[key] = value
            self._collection_ref().document(str(doc["_id"])).set(doc)
            return

        target = self.find_one(query)
        if not target:
            return
        if "$set" in update:
            target.update(update["$set"])
            self._database._memory_store.setdefault(self._name, {})[str(target["_id"])] = target

    def delete_one(self, query):
        if self._client is not None:
            for doc in self._docs():
                if self._match(doc, query):
                    self._collection_ref().document(str(doc["_id"])).delete()
                    break
            return
        for key, doc in list(self._database._memory_store.get(self._name, {}).items()):
            if self._match(doc, query):
                del self._database._memory_store[self._name][key]
                return

    def delete_many(self, query):
        for doc in list(self._docs()):
            if self._match(doc, query):
                self.delete_one({"_id": doc.get("_id")})

    def count_documents(self, query=None):
        return sum(1 for doc in self._docs() if self._match(doc, query or {}))

    def create_index(self, *args, **kwargs):
        return None

    def aggregate(self, pipeline):
        docs = self._docs()
        if not pipeline:
            return []
        match_stage = next((stage for stage in pipeline if "$match" in stage), None)
        if match_stage:
            docs = [doc for doc in docs if self._match(doc, match_stage["$match"])]
        group_stage = next((stage for stage in pipeline if "$group" in stage), None)
        if not group_stage:
            return docs
        group_key = group_stage["$group"].get("_id")
        if group_key == "$status":
            result = {}
            for doc in docs:
                key = doc.get("status")
                result[key] = result.get(key, 0) + 1
            return [{"_id": k, "count": v} for k, v in result.items()]
        if isinstance(group_key, str) and group_key.startswith("$"):
            field = group_key[1:]
            result = {}
            for doc in docs:
                key = doc.get(field)
                result[key] = result.get(key, 0) + 1
            return [{"_id": k, "count": v} for k, v in result.items()]
        return []


class FirestoreDatabase:
    def __init__(self, client=None):
        self._memory_store = {}
        self._client = client

    def __getitem__(self, name):
        return FirestoreCollection(self, name, self._client)

    def __getattr__(self, name):
        return self[name]


def _use_firestore():
    fire_project = os.getenv("FIRESTORE_PROJECT_ID") or os.getenv("FIREBASE_PROJECT_ID")
    return os.getenv("USE_FIRESTORE", "false").lower() in {"1", "true", "yes", "on"} or bool(fire_project)


def _init_firestore_client(app):
    if firebase_admin is None or firestore is None:
        return None
    project_id = os.getenv("FIRESTORE_PROJECT_ID") or os.getenv("FIREBASE_PROJECT_ID") or os.getenv("GCLOUD_PROJECT")
    if not project_id:
        return None

    try:
        if not firebase_admin._apps:
            json_blob = (
                os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
                or os.getenv("FIREBASE_SERVICE_ACCOUNT")
                or os.getenv("GOOGLE_CREDENTIALS_JSON")
                or os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
            )
            if json_blob:
                try:
                    service_account = json.loads(json_blob)
                    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
                        json.dump(service_account, tmp)
                        tmp_path = tmp.name
                    cred = credentials.Certificate(tmp_path)
                    firebase_admin.initialize_app(cred, {"projectId": project_id})
                    os.unlink(tmp_path)
                except Exception:
                    cred = credentials.ApplicationDefault()
                    firebase_admin.initialize_app(cred, {"projectId": project_id})
            else:
                cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(cred, {"projectId": project_id})
        return firestore.client()
    except Exception as exc:  # pragma: no cover
        app.logger.warning("Firestore unavailable: %s", exc)
        return None


def _seed_default_admin_if_needed(app):
    """Create the demo admin account for local/development setups."""
    db = get_db()
    if db.admins.count_documents({"email": "admin@yourbrand.com"}) == 0:
        db.admins.insert_one({
            "name": "Studio Admin",
            "email": "admin@yourbrand.com",
            "password_hash": generate_password_hash("ChangeMe123!"),
            "role": "super_admin",
            "created_at": datetime.now(timezone.utc),
            "last_login": None,
        })
        app.logger.warning("Created default admin account: admin@yourbrand.com / ChangeMe123!")


def init_db(app):
    """Initialize the configured database backend."""
    global _client, _db
    uri = app.config.get("MONGO_URI")
    if uri and not _use_firestore():
        try:
            _client = MongoClient(
                uri,
                serverSelectionTimeoutMS=8000,
                tls=True,
                tlsCAFile=certifi.where(),
            )
            _db = _client[app.config["DB_NAME"]]
            _client.admin.command("ping")
            _ensure_indexes(_db)
            if app.config.get("DEBUG"):
                _seed_default_admin_if_needed(app)
            app.logger.info("Connected to MongoDB Atlas: %s", app.config["DB_NAME"])
            return _db
        except Exception as e:  # pragma: no cover
            app.logger.warning("MongoDB Atlas unreachable, falling back to Firestore/mock: %s", e)

    firestore_client = _init_firestore_client(app) if _use_firestore() else None
    if firestore_client is not None:
        _client = firestore_client
        _db = FirestoreDatabase(firestore_client)
        _ensure_indexes(_db)
        _seed_default_admin_if_needed(app)
        app.logger.info("Connected to Firestore project: %s", firestore_client.project)
        return _db

    allow_mock = os.getenv("USE_MOCK_DB", "true").lower() in {"1", "true", "yes", "on"}
    if not allow_mock:
        raise RuntimeError("Could not reach MongoDB Atlas or Firestore. Check your database configuration.")
    app.logger.warning("Using in-memory Mongo-compatible mock database.")
    _client = mongomock.MongoClient()
    _db = _client[app.config["DB_NAME"]]
    _ensure_indexes(_db)
    _seed_default_admin_if_needed(app)
    return _db


def _ensure_indexes(db):
    """Create indexes used across the app. Safe to call repeatedly (idempotent)."""
    for collection_name in [
        "admins",
        "bookings",
        "contacts",
        "services",
        "pricing_packages",
        "blogs",
        "testimonials",
        "website_settings",
    ]:
        try:
            getattr(db, collection_name)
        except Exception:
            pass


def get_db():
    """Return the active database handle. init_db(app) must have run first."""
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_db(app) first.")
    return _db


def _ensure_indexes(db: Database):
    """Create indexes used across the app. Safe to call repeatedly (idempotent)."""
    db.admins.create_index("email", unique=True)
    db.bookings.create_index("created_at")
    db.bookings.create_index("status")
    db.bookings.create_index("event_date")
    db.contacts.create_index("created_at")
    db.contacts.create_index("is_read")
    db.services.create_index("slug", unique=True)
    db.pricing_packages.create_index("order")
    db.blogs.create_index("slug", unique=True)
    db.blogs.create_index("published_at")
    db.testimonials.create_index("is_featured")
    db.website_settings.create_index("key", unique=True)


def get_db() -> Database:
    """Return the active database handle. init_db() must have run first."""
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_db(app) first.")
    return _db
