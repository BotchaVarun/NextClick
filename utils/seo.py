"""
SEO helpers: builds per-page meta tag context and generates
sitemap.xml / robots.txt content and Schema.org JSON-LD.
"""
import json
from flask import current_app


def page_meta(title=None, description=None, image=None, url=None):
    """Returns a dict injected into templates for <title>/meta tags/OpenGraph."""
    site_name = current_app.config["SITE_NAME"]
    return {
        "title": f"{title} | {site_name}" if title else site_name,
        "description": description or f"{site_name} - professional photography services.",
        "image": image or f"{current_app.config['SITE_URL']}/static/images/backgrounds/og-default.jpg",
        "url": url or current_app.config["SITE_URL"],
    }


def local_business_schema(settings: dict):
    """Schema.org JSON-LD for a local photography business (rich snippets in search)."""
    schema = {
        "@context": "https://schema.org",
        "@type": "PhotographyBusiness",
        "name": settings.get("site_name", current_app.config["SITE_NAME"]),
        "description": settings.get("tagline", ""),
        "telephone": settings.get("phone", ""),
        "email": settings.get("email", ""),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": settings.get("address", ""),
        },
        "url": current_app.config["SITE_URL"],
        "sameAs": [
            settings.get("instagram", ""),
            settings.get("facebook", ""),
            settings.get("pinterest", ""),
        ],
    }
    return json.dumps(schema)


def generate_sitemap_urls(blog_slugs, service_slugs):
    """Returns a list of (url, priority) tuples for sitemap.xml generation."""
    base = current_app.config["SITE_URL"]
    static_pages = [
        ("/", "1.0"), ("/about", "0.8"), ("/services", "0.9"),
        ("/pricing", "0.8"), ("/testimonials", "0.6"), ("/blog", "0.7"),
        ("/contact", "0.7"), ("/booking", "0.9"), ("/faq", "0.5"),
    ]
    urls = [(base + path, priority) for path, priority in static_pages]
    urls += [(f"{base}/services/{s}", "0.7") for s in service_slugs]
    urls += [(f"{base}/blog/{s}", "0.6") for s in blog_slugs]
    return urls
