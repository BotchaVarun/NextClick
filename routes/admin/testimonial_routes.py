from flask import Blueprint, render_template, request, redirect, url_for, flash
from middleware.auth_middleware import admin_required
from models.testimonial import Testimonial
from utils.cloudinary_service import upload_image

admin_testimonial_bp = Blueprint("admin_testimonial", __name__)


@admin_testimonial_bp.route("/testimonials")
@admin_required
def testimonials():
    items = Testimonial.find_all()
    return render_template("admin/testimonials.html", testimonials=items)


@admin_testimonial_bp.route("/testimonials/create", methods=["POST"])
@admin_required
def create():
    photo_url = upload_image(request.files.get("photo"), folder="testimonials")
    Testimonial.create({
        "client_name": request.form.get("client_name", ""),
        "event_type": request.form.get("event_type", ""),
        "quote": request.form.get("quote", ""),
        "rating": request.form.get("rating", 5),
        "photo_url": photo_url or "",
        "is_featured": bool(request.form.get("is_featured")),
    })
    flash("Testimonial added.", "success")
    return redirect(url_for("admin_testimonial.testimonials"))


@admin_testimonial_bp.route("/testimonials/<t_id>/update", methods=["POST"])
@admin_required
def update(t_id):
    photo_url = upload_image(request.files.get("photo"), folder="testimonials")
    data = {
        "client_name": request.form.get("client_name"),
        "event_type": request.form.get("event_type"),
        "quote": request.form.get("quote"),
        "rating": request.form.get("rating"),
        "is_featured": bool(request.form.get("is_featured")),
    }
    if photo_url:
        data["photo_url"] = photo_url
    Testimonial.update(t_id, data)
    flash("Testimonial updated.", "success")
    return redirect(url_for("admin_testimonial.testimonials"))


@admin_testimonial_bp.route("/testimonials/<t_id>/delete", methods=["POST"])
@admin_required
def delete(t_id):
    Testimonial.delete(t_id)
    flash("Testimonial deleted.", "success")
    return redirect(url_for("admin_testimonial.testimonials"))
