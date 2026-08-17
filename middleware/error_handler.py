"""Registers friendly error pages for the whole app."""
from flask import render_template


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return render_template("public/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        app.logger.error("Server error: %s", e)
        return render_template("public/500.html"), 500

    @app.errorhandler(429)
    def too_many_requests(e):
        return render_template("public/500.html", message="Too many requests. Please slow down."), 429

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("public/404.html", message="Access denied."), 403
