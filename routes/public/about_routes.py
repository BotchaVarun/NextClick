from flask import Blueprint, render_template
from models.website_settings import WebsiteSettings
from utils.seo import page_meta

about_bp = Blueprint("about", __name__)


@about_bp.route("/about")
def about():
    settings = WebsiteSettings.get()
    meta = page_meta(title="About Us", description="Learn about our studio, our story, and our approach.")
    return render_template("public/about.html", settings=settings, meta=meta)
