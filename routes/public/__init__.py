"""
Registers every public blueprint on the Flask app in one place,
so app.py only needs to import register_public_routes().
"""


def register_public_routes(app):
    from routes.public.home_routes import home_bp
    from routes.public.about_routes import about_bp
    from routes.public.services_routes import services_bp
    from routes.public.pricing_routes import pricing_bp
    from routes.public.blog_routes import blog_bp
    from routes.public.contact_routes import contact_bp
    from routes.public.booking_routes import booking_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(pricing_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(booking_bp)
