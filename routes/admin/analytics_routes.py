from flask import Blueprint, render_template
from middleware.auth_middleware import admin_required
from services.analytics_service import dashboard_summary

admin_analytics_bp = Blueprint("admin_analytics", __name__)


@admin_analytics_bp.route("/analytics")
@admin_required
def analytics():
    summary = dashboard_summary()
    return render_template("admin/analytics.html", summary=summary)
