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

    # ==========================
    # Authentication
    # ==========================
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    # ==========================
    # Dashboard
    # ==========================
    from app.dashboard.routes import dashboard_bp
    app.register_blueprint(dashboard_bp)

    # ==========================
    # EC2
    # ==========================
    from app.ec2.routes import ec2_bp
    app.register_blueprint(ec2_bp)

    # ==========================
    # Security Groups
    # ==========================
    from app.security_groups.routes import sg_bp
    app.register_blueprint(sg_bp)

    # ==========================
    # IAM
    # ==========================
    from app.iam.routes import iam_bp
    app.register_blueprint(iam_bp)

    # ==========================
    # S3
    # ==========================
    from app.s3.routes import s3_bp
    app.register_blueprint(s3_bp)
    
    # ==========================
    # Reports
    # ==========================
    from app.reports.routes import reports_bp
    app.register_blueprint(reports_bp)

    # ==========================
    # API
    # ==========================
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    # ==========================
    # Settings
    # ==========================
    from app.settings.routes import settings_bp
    app.register_blueprint(settings_bp)

    return app
