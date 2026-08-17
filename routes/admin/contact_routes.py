from flask import Blueprint, render_template, request, redirect, url_for, flash
from middleware.auth_middleware import admin_required
from models.contact import Contact

admin_contact_bp = Blueprint("admin_contact", __name__)


@admin_contact_bp.route("/contacts")
@admin_required
def contacts():
    unread_only = request.args.get("unread") == "1"
    page = request.args.get("page", 1, type=int)
    items, total = Contact.find_all(unread_only=unread_only, page=page, per_page=15)
    total_pages = max(1, (total + 14) // 15)
    return render_template(
        "admin/contacts.html", contacts=items, unread_only=unread_only,
        page=page, total_pages=total_pages,
    )


@admin_contact_bp.route("/contacts/<contact_id>/read", methods=["POST"])
@admin_required
def mark_read(contact_id):
    Contact.mark_read(contact_id)
    return redirect(url_for("admin_contact.contacts"))


@admin_contact_bp.route("/contacts/<contact_id>/delete", methods=["POST"])
@admin_required
def delete_contact(contact_id):
    Contact.delete(contact_id)
    flash("Message deleted.", "success")
    return redirect(url_for("admin_contact.contacts"))
