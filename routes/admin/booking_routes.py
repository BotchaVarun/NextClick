from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from middleware.auth_middleware import admin_required
from models.booking import Booking

admin_booking_bp = Blueprint("admin_booking", __name__)


@admin_booking_bp.route("/bookings")
@admin_required
def bookings():
    status = request.args.get("status", "all")
    page = request.args.get("page", 1, type=int)
    items, total = Booking.find_all(status=status, page=page, per_page=15)
    total_pages = max(1, (total + 14) // 15)
    return render_template(
        "admin/bookings.html", bookings=items, status=status,
        page=page, total_pages=total_pages,
    )


@admin_booking_bp.route("/bookings/<booking_id>/status", methods=["POST"])
@admin_required
def update_status(booking_id):
    new_status = request.form.get("status")
    try:
        Booking.update_status(booking_id, new_status)
        flash("Booking status updated.", "success")
    except ValueError:
        flash("Invalid status value.", "error")
    return redirect(url_for("admin_booking.bookings"))


@admin_booking_bp.route("/bookings/<booking_id>/delete", methods=["POST"])
@admin_required
def delete_booking(booking_id):
    Booking.delete(booking_id)
    flash("Booking deleted.", "success")
    return redirect(url_for("admin_booking.bookings"))
