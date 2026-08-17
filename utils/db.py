"""
Thin convenience re-export so route/service modules can simply do:
    from utils.db import get_db
instead of reaching into database.mongodb directly.
"""
from database.mongodb import get_db  # noqa: F401
