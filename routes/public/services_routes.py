from flask import Blueprint, render_template, abort
from models.service import Service
from utils.seo import page_meta

services_bp = Blueprint("services", __name__)


@services_bp.route("/services")
def services_list():
    services = Service.find_all()
    meta = page_meta(title="Our Services", description="Explore our full range of photography services.")
    return render_template("public/services.html", services=services, meta=meta)


@services_bp.route("/services/<slug>")
def service_detail(slug):
    service = Service.find_by_slug(slug)
    if not service:
        abort(404)
    meta = page_meta(title=service["title"], description=service.get("short_description", ""))
    return render_template("public/services.html", service=service, single=True, meta=meta)
