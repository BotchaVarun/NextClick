"""
Role-based access decorator, layered on top of Flask-Login's login_required.
Use @admin_required for routes any logged-in admin can access,
and @role_required("super_admin") for routes restricted to a specific role.
"""
from functools import wraps
from flask import abort
from flask_login import current_user, login_required


def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(*args, **kwargs):
        return view_func(*args, **kwargs)
    return wrapper


def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(*args, **kwargs):
            if current_user.role != role:
                abort(403)
            return view_func(*args, **kwargs)
        return wrapper
    return decorator
