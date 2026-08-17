"""Registers every admin blueprint on the Flask app, all under /admin."""


def register_admin_routes(app):
    from routes.admin.auth_routes import auth_bp
    from routes.admin.dashboard_routes import dashboard_bp
    from routes.admin.booking_routes import admin_booking_bp
    from routes.admin.contact_routes import admin_contact_bp
    from routes.admin.services_routes import admin_services_bp
    from routes.admin.pricing_routes import admin_pricing_bp
    from routes.admin.blog_routes import admin_blog_bp
    from routes.admin.testimonial_routes import admin_testimonial_bp
    from routes.admin.settings_routes import admin_settings_bp
    from routes.admin.seo_routes import admin_seo_bp
    from routes.admin.analytics_routes import admin_analytics_bp
    from routes.admin.profile_routes import admin_profile_bp

    app.register_blueprint(auth_bp, url_prefix="/admin")
    app.register_blueprint(dashboard_bp, url_prefix="/admin")
    app.register_blueprint(admin_booking_bp, url_prefix="/admin")
    app.register_blueprint(admin_contact_bp, url_prefix="/admin")
    app.register_blueprint(admin_services_bp, url_prefix="/admin")
    app.register_blueprint(admin_pricing_bp, url_prefix="/admin")
    app.register_blueprint(admin_blog_bp, url_prefix="/admin")
    app.register_blueprint(admin_testimonial_bp, url_prefix="/admin")
    app.register_blueprint(admin_settings_bp, url_prefix="/admin")
    app.register_blueprint(admin_seo_bp, url_prefix="/admin")
    app.register_blueprint(admin_analytics_bp, url_prefix="/admin")
    app.register_blueprint(admin_profile_bp, url_prefix="/admin")
