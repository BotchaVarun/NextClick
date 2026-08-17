"""Business logic for blog listing/pagination on the public site."""
from models.blog import Blog


def get_published_page(page: int, per_page: int):
    posts, total = Blog.find_published(page=page, per_page=per_page)
    total_pages = max(1, (total + per_page - 1) // per_page)
    return posts, total, total_pages
