from flask import Blueprint, render_template, request, redirect, url_for, flash
from middleware.auth_middleware import role_required
from models.website_settings import WebsiteSettings
from utils.cloudinary_service import upload_image

admin_settings_bp = Blueprint("admin_settings", __name__)


@admin_settings_bp.route("/settings")
@role_required("super_admin")
def settings():
    values = WebsiteSettings.get("general")
    return render_template("admin/settings.html", settings=values)


@admin_settings_bp.route("/settings/update", methods=["POST"])
@role_required("super_admin")
def update():
    current = WebsiteSettings.get("general")
    hero_image = current.get("hero_image", "")
    uploaded = upload_image(request.files.get("hero_image"), folder="hero")
    if uploaded:
        hero_image = uploaded

    values = {
        "site_name": request.form.get("site_name", ""),
        "tagline": request.form.get("tagline", ""),
        "phone": request.form.get("phone", ""),
        "whatsapp_number": request.form.get("whatsapp_number", "").strip(),
        "email": request.form.get("email", ""),
        "address": request.form.get("address", ""),
        "instagram": request.form.get("instagram", ""),
        "facebook": request.form.get("facebook", ""),
        "pinterest": request.form.get("pinterest", ""),
        "primary_color": request.form.get("primary_color", "#1C1C1E"),
        "accent_color": request.form.get("accent_color", "#C9A46A"),
        "hero_image": hero_image,
    }
    WebsiteSettings.update("general", values)
    flash("Website settings updated.", "success")
    return redirect(url_for("admin_settings.settings"))
