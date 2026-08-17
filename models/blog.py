"""Blog model - wraps the `blogs` collection."""
from datetime import datetime, timezone
from bson.objectid import ObjectId
from slugify import slugify
from database.mongodb import get_db


class Blog:
    @staticmethod
    def _col():
        return get_db().blogs

    @staticmethod
    def create(data: dict):
        doc = {
            "title": data["title"].strip(),
            "slug": slugify(data["title"]),
            "excerpt": data.get("excerpt", "").strip(),
            "content": data.get("content", ""),
            "cover_image_url": data.get("cover_image_url", ""),
            "author": data.get("author", "Studio Team"),
            "tags": data.get("tags", []),
            "meta_title": data.get("meta_title", data["title"]),
            "meta_description": data.get("meta_description", data.get("excerpt", "")),
            "is_published": data.get("is_published", False),
            "published_at": datetime.now(timezone.utc) if data.get("is_published") else None,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        result = Blog._col().insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    @staticmethod
    def find_published(page=1, per_page=6):
        skip = (page - 1) * per_page
        query = {"is_published": True}
        cursor = Blog._col().find(query).sort("published_at", -1).skip(skip).limit(per_page)
        total = Blog._col().count_documents(query)
        return list(cursor), total

    @staticmethod
    def find_all(page=1, per_page=15):
        skip = (page - 1) * per_page
        cursor = Blog._col().find({}).sort("created_at", -1).skip(skip).limit(per_page)
        total = Blog._col().count_documents({})
        return list(cursor), total

    @staticmethod
    def find_by_slug(slug):
        return Blog._col().find_one({"slug": slug, "is_published": True})

    @staticmethod
    def find_by_id(blog_id):
        try:
            return Blog._col().find_one({"_id": ObjectId(blog_id)})
        except Exception:
            return None

    @staticmethod
    def update(blog_id, data: dict):
        updates = {k: v for k, v in data.items() if v is not None}
        if "title" in updates:
            updates["slug"] = slugify(updates["title"])
        if updates.get("is_published") is True:
            existing = Blog.find_by_id(blog_id)
            if existing and not existing.get("published_at"):
                updates["published_at"] = datetime.now(timezone.utc)
        updates["updated_at"] = datetime.now(timezone.utc)
        Blog._col().update_one({"_id": ObjectId(blog_id)}, {"$set": updates})

    @staticmethod
    def delete(blog_id):
        Blog._col().delete_one({"_id": ObjectId(blog_id)})
