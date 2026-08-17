from flask import Blueprint, render_template, request, redirect, url_for, flash
from middleware.auth_middleware import role_required
from models.website_settings import WebsiteSettings

admin_seo_bp = Blueprint("admin_seo", __name__)


@admin_seo_bp.route("/seo")
@role_required("super_admin")
def seo():
    values = WebsiteSettings.get("seo_defaults")
    return render_template("admin/seo.html", seo=values)


@admin_seo_bp.route("/seo/update", methods=["POST"])
@role_required("super_admin")
def update():
    values = {
        "default_meta_title": request.form.get("default_meta_title", ""),
        "default_meta_description": request.form.get("default_meta_description", ""),
        "ga4_measurement_id": request.form.get("ga4_measurement_id", ""),
        "google_search_console_verification": request.form.get("google_search_console_verification", ""),
    }
    WebsiteSettings.update("seo_defaults", values)
    flash("SEO settings updated.", "success")
    return redirect(url_for("admin_seo.seo"))
