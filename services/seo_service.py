"""Business logic for generating sitemap.xml and robots.txt content."""
from models.blog import Blog
from models.service import Service
from utils.seo import generate_sitemap_urls


def build_sitemap_xml():
    blogs, _ = Blog.find_published(page=1, per_page=1000)
    services = Service.find_all(active_only=True)
    blog_slugs = [b["slug"] for b in blogs]
    service_slugs = [s["slug"] for s in services]

    urls = generate_sitemap_urls(blog_slugs, service_slugs)
    entries = "\n".join(
        f"  <url><loc>{url}</loc><priority>{priority}</priority></url>"
        for url, priority in urls
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n"
        "</urlset>"
    )


def build_robots_txt(site_url):
    return (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin/\n\n"
        f"Sitemap: {site_url}/sitemap.xml\n"
    )
