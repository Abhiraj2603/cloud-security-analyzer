import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-before-production")

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "app.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REPORT_FOLDER = os.path.join(BASE_DIR, "reports")
    LOG_FOLDER = os.path.join(BASE_DIR, "logs")
