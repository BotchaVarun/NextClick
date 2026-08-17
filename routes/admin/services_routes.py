from flask import Blueprint, render_template, request, redirect, url_for, flash
from middleware.auth_middleware import admin_required
from models.service import Service
from utils.cloudinary_service import upload_image

admin_services_bp = Blueprint("admin_services", __name__)


@admin_services_bp.route("/services")
@admin_required
def services():
    items = Service.find_all(active_only=False)
    return render_template("admin/services.html", services=items)


@admin_services_bp.route("/services/create", methods=["POST"])
@admin_required
def create():
    image_url = upload_image(request.files.get("image"), folder="services")
    Service.create({
        "title": request.form.get("title", ""),
        "short_description": request.form.get("short_description", ""),
        "description": request.form.get("description", ""),
        "icon": request.form.get("icon", "camera"),
        "image_url": image_url or "",
        "order": request.form.get("order", 0),
        "is_active": bool(request.form.get("is_active")),
    })
    flash("Service created.", "success")
    return redirect(url_for("admin_services.services"))


@admin_services_bp.route("/services/<service_id>/update", methods=["POST"])
@admin_required
def update(service_id):
    image_url = upload_image(request.files.get("image"), folder="services")
    data = {
        "title": request.form.get("title"),
        "short_description": request.form.get("short_description"),
        "description": request.form.get("description"),
        "icon": request.form.get("icon"),
        "order": request.form.get("order"),
        "is_active": bool(request.form.get("is_active")),
    }
    if image_url:
        data["image_url"] = image_url
    Service.update(service_id, data)
    flash("Service updated.", "success")
    return redirect(url_for("admin_services.services"))


@admin_services_bp.route("/services/<service_id>/delete", methods=["POST"])
@admin_required
def delete(service_id):
    Service.delete(service_id)
    flash("Service deleted.", "success")
    return redirect(url_for("admin_services.services"))
