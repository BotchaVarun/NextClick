from flask import Blueprint, render_template, request, abort, current_app
from models.blog import Blog
from services.blog_service import get_published_page
from utils.seo import page_meta
from utils.helpers import paginate_range

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/blog")
def blog_list():
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config["BLOG_POSTS_PER_PAGE"]
    posts, total, total_pages = get_published_page(page, per_page)
    meta = page_meta(title="Blog", description="Photography tips, behind-the-scenes stories, and inspiration.")
    return render_template(
        "public/blog.html",
        posts=posts,
        page=page,
        total_pages=total_pages,
        page_range=paginate_range(page, total_pages),
        meta=meta,
    )


@blog_bp.route("/blog/<slug>")
def blog_detail(slug):
    post = Blog.find_by_slug(slug)
    if not post:
        abort(404)
    meta = page_meta(
        title=post.get("meta_title", post["title"]),
        description=post.get("meta_description", post.get("excerpt", "")),
        image=post.get("cover_image_url"),
    )
    return render_template("public/blog_details.html", post=post, meta=meta)
