from flask import Blueprint, render_template, Response
from models.service import Service
from models.pricing import Pricing
from models.testimonial import Testimonial
from models.website_settings import WebsiteSettings

from utils.seo import page_meta
from services.seo_service import build_sitemap_xml, build_robots_txt
from flask import current_app

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():
    settings = WebsiteSettings.get()
    services = Service.find_all()[:3]
    packages = Pricing.find_all()
    testimonials = Testimonial.find_all(featured_only=True)[:6]
    meta = page_meta(
        title="Home",
        description=settings.get("tagline", "Professional photography services."),
    )
    return render_template(
        "public/index.html",
        settings=settings,
        services=services,
        packages=packages,
        testimonials=testimonials,
        meta=meta,
    )


@home_bp.route("/testimonials")
def testimonials():
    items = Testimonial.find_all()
    meta = page_meta(title="Testimonials", description="Hear what our clients have to say.")
    return render_template("public/testimonials.html", testimonials=items, meta=meta)


@home_bp.route("/faq")
def faq():
    meta = page_meta(title="FAQ", description="Frequently asked questions.")
    return render_template("public/faq.html", meta=meta)


@home_bp.route("/privacy-policy")
def privacy_policy():
    meta = page_meta(title="Privacy Policy")
    return render_template("public/privacy_policy.html", meta=meta)


@home_bp.route("/terms")
def terms():
    meta = page_meta(title="Terms & Conditions")
    return render_template("public/terms.html", meta=meta)


@home_bp.route("/sitemap.xml")
def sitemap():
    xml = build_sitemap_xml()
    return Response(xml, mimetype="application/xml")


@home_bp.route("/robots.txt")
def robots():
    txt = build_robots_txt(current_app.config["SITE_URL"])
    return Response(txt, mimetype="text/plain")
