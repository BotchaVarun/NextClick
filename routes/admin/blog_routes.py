from flask import Blueprint, render_template, request, redirect, url_for, flash
from middleware.auth_middleware import admin_required
from models.blog import Blog
from utils.cloudinary_service import upload_image

admin_blog_bp = Blueprint("admin_blog", __name__)


@admin_blog_bp.route("/blog")
@admin_required
def blog():
    page = request.args.get("page", 1, type=int)
    posts, total = Blog.find_all(page=page, per_page=15)
    total_pages = max(1, (total + 14) // 15)
    return render_template("admin/blog.html", posts=posts, page=page, total_pages=total_pages)


@admin_blog_bp.route("/blog/create", methods=["POST"])
@admin_required
def create():
    cover_url = upload_image(request.files.get("cover_image"), folder="blog")
    tags = [t.strip() for t in request.form.get("tags", "").split(",") if t.strip()]
    Blog.create({
        "title": request.form.get("title", ""),
        "excerpt": request.form.get("excerpt", ""),
        "content": request.form.get("content", ""),
        "cover_image_url": cover_url or "",
        "author": request.form.get("author", "Studio Team"),
        "tags": tags,
        "meta_title": request.form.get("meta_title", ""),
        "meta_description": request.form.get("meta_description", ""),
        "is_published": bool(request.form.get("is_published")),
    })
    flash("Blog post created.", "success")
    return redirect(url_for("admin_blog.blog"))


@admin_blog_bp.route("/blog/<blog_id>/update", methods=["POST"])
@admin_required
def update(blog_id):
    cover_url = upload_image(request.files.get("cover_image"), folder="blog")
    tags = [t.strip() for t in request.form.get("tags", "").split(",") if t.strip()]
    data = {
        "title": request.form.get("title"),
        "excerpt": request.form.get("excerpt"),
        "content": request.form.get("content"),
        "author": request.form.get("author"),
        "tags": tags,
        "meta_title": request.form.get("meta_title"),
        "meta_description": request.form.get("meta_description"),
        "is_published": bool(request.form.get("is_published")),
    }
    if cover_url:
        data["cover_image_url"] = cover_url
    Blog.update(blog_id, data)
    flash("Blog post updated.", "success")
    return redirect(url_for("admin_blog.blog"))


@admin_blog_bp.route("/blog/<blog_id>/delete", methods=["POST"])
@admin_required
def delete(blog_id):
    Blog.delete(blog_id)
    flash("Blog post deleted.", "success")
    return redirect(url_for("admin_blog.blog"))
