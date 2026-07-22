from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object("app.config.Config")

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Authentication
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    # Dashboard
    from app.dashboard.routes import dashboard_bp
    app.register_blueprint(dashboard_bp)

    # API
    from app.api.routes import api_bp
    app.register_blueprint(api_bp)

    # Settings
    from app.settings.routes import settings_bp
    app.register_blueprint(settings_bp)

    return app
