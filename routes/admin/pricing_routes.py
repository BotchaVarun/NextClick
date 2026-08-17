from flask import Blueprint, render_template, request, redirect, url_for, flash
from middleware.auth_middleware import admin_required
from models.pricing import Pricing

admin_pricing_bp = Blueprint("admin_pricing", __name__)


@admin_pricing_bp.route("/pricing")
@admin_required
def pricing():
    packages = Pricing.find_all(active_only=False)
    return render_template("admin/pricing.html", packages=packages)


@admin_pricing_bp.route("/pricing/create", methods=["POST"])
@admin_required
def create():
    features = [f.strip() for f in request.form.get("features", "").split(",") if f.strip()]
    Pricing.create({
        "name": request.form.get("name", ""),
        "price": request.form.get("price", 0),
        "duration": request.form.get("duration", ""),
        "features": features,
        "is_popular": bool(request.form.get("is_popular")),
        "order": request.form.get("order", 0),
        "is_active": bool(request.form.get("is_active")),
    })
    flash("Package created.", "success")
    return redirect(url_for("admin_pricing.pricing"))


@admin_pricing_bp.route("/pricing/<pkg_id>/update", methods=["POST"])
@admin_required
def update(pkg_id):
    features = [f.strip() for f in request.form.get("features", "").split(",") if f.strip()]
    Pricing.update(pkg_id, {
        "name": request.form.get("name"),
        "price": float(request.form.get("price", 0)),
        "duration": request.form.get("duration"),
        "features": features,
        "is_popular": bool(request.form.get("is_popular")),
        "order": request.form.get("order"),
        "is_active": bool(request.form.get("is_active")),
    })
    flash("Package updated.", "success")
    return redirect(url_for("admin_pricing.pricing"))


@admin_pricing_bp.route("/pricing/<pkg_id>/delete", methods=["POST"])
@admin_required
def delete(pkg_id):
    Pricing.delete(pkg_id)
    flash("Package deleted.", "success")
    return redirect(url_for("admin_pricing.pricing"))
