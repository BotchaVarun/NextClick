from flask import Blueprint, render_template
from models.pricing import Pricing
from utils.seo import page_meta

pricing_bp = Blueprint("pricing", __name__)


@pricing_bp.route("/pricing")
def pricing_list():
    packages = Pricing.find_all()
    meta = page_meta(title="Pricing", description="Transparent, all-inclusive photography packages.")
    return render_template("public/pricing.html", packages=packages, meta=meta)
