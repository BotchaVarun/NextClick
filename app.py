"""
Application factory.
Keeps app.py minimal: initializes extensions, registers blueprints,
error handlers, and template filters. Actual logic lives in routes/models/services.
"""
from flask import Flask
from flask_wtf import CSRFProtect

from config import get_config
from database.mongodb import init_db
from utils.auth import init_auth
from utils.email_service import init_mail
from utils.cloudinary_service import init_cloudinary
from utils.logger import setup_logger
from utils.helpers import format_date, currency, truncate_words
from middleware.security import init_security
from middleware.error_handler import register_error_handlers
from routes.public import register_public_routes
from routes.admin import register_admin_routes

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    # --- Extensions ---
    csrf.init_app(app)
    init_auth(app)
    init_mail(app)
    if app.config.get("CLOUDINARY_CLOUD_NAME"):
        init_cloudinary(app)
    init_security(app)
    setup_logger(app)

    # --- Database ---
    init_db(app)

    # --- Blueprints ---
    register_public_routes(app)
    register_admin_routes(app)

    # --- Error handlers ---
    register_error_handlers(app)

    # --- Template filters/globals (used across all templates) ---
    app.jinja_env.filters["format_date"] = format_date
    app.jinja_env.filters["currency"] = currency
    app.jinja_env.filters["truncate_words"] = truncate_words
    app.jinja_env.globals["site_name"] = app.config["SITE_NAME"]
    app.jinja_env.globals["ga4_id"] = app.config["GA4_MEASUREMENT_ID"]

    from datetime import datetime
    app.jinja_env.globals["current_year"] = datetime.now().year

    return app


# Module-level app instance for `flask run` / gunicorn discovery via `app:app`
app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
