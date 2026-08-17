from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.admin import Admin
from middleware.security import rate_limit

auth_bp = Blueprint("admin_auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin_dashboard.dashboard"))

    if request.method == "POST":
        rate_limit("admin_login", max_requests=8, window_seconds=300)
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        admin = Admin.find_by_email(email)
        if admin and admin.check_password(password):
            login_user(admin, remember=remember)
            admin.record_login()
            flash(f"Welcome back, {admin.name}.", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("admin_dashboard.dashboard"))

        flash("Invalid email or password.", "error")

    return render_template("admin/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out.", "success")
    return redirect(url_for("admin_auth.login"))
