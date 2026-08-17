"""
Security headers + a minimal in-memory rate limiter for public form endpoints
(booking/contact) to deter basic spam/abuse without adding an external service.
"""
import time
from collections import defaultdict
from flask import request, abort

_hits = defaultdict(list)


def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


def rate_limit(key_prefix, max_requests=5, window_seconds=60):
    """Simple sliding-window limiter keyed by IP. Good enough for a single-instance app."""
    ip = request.remote_addr or "unknown"
    key = f"{key_prefix}:{ip}"
    now = time.time()
    _hits[key] = [t for t in _hits[key] if now - t < window_seconds]
    if len(_hits[key]) >= max_requests:
        abort(429, description="Too many requests. Please try again shortly.")
    _hits[key].append(now)


def init_security(app):
    app.after_request(add_security_headers)
