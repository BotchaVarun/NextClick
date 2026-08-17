"""Misc template/view helper functions."""
from datetime import datetime


def format_date(value, fmt="%B %d, %Y"):
    if not value:
        return ""
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except ValueError:
            return value
    return value.strftime(fmt)


def currency(value):
    try:
        return f"${float(value):,.0f}"
    except (TypeError, ValueError):
        return value


def truncate_words(text, count=25):
    if not text:
        return ""
    words = text.split()
    if len(words) <= count:
        return text
    return " ".join(words[:count]) + "..."


def paginate_range(current_page, total_pages, window=2):
    """Returns a list of page numbers (with None as an ellipsis marker) for pagination UI."""
    pages = []
    for p in range(1, total_pages + 1):
        if p == 1 or p == total_pages or abs(p - current_page) <= window:
            pages.append(p)
        elif pages and pages[-1] is not None:
            pages.append(None)
    return pages
