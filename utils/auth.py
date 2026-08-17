"""Flask-Login wiring: user_loader callback and login manager setup."""
from flask_login import LoginManager
from models.admin import Admin

login_manager = LoginManager()
login_manager.login_view = "admin_auth.login"
login_manager.login_message = "Please log in to access the admin panel."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    return Admin.find_by_id(user_id)


def init_auth(app):
    login_manager.init_app(app)
