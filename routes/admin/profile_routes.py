from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from middleware.auth_middleware import admin_required

admin_profile_bp = Blueprint("admin_profile", __name__)


@admin_profile_bp.route("/profile")
@admin_required
def profile():
    return render_template("admin/profile.html")


@admin_profile_bp.route("/profile/update", methods=["POST"])
@admin_required
def update():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    current_user.update_profile(name=name, email=email)
    flash("Profile updated.", "success")
    return redirect(url_for("admin_profile.profile"))


@admin_profile_bp.route("/profile/password", methods=["POST"])
@admin_required
def change_password():
    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not current_user.check_password(current_password):
        flash("Current password is incorrect.", "error")
    elif new_password != confirm_password:
        flash("New passwords do not match.", "error")
    elif len(new_password) < 8:
        flash("New password must be at least 8 characters.", "error")
    else:
        current_user.update_password(new_password)
        flash("Password changed successfully.", "success")

    return redirect(url_for("admin_profile.profile"))
