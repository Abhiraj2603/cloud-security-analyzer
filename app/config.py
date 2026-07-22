import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    # ------------------------
    # Flask
    # ------------------------
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "change-this-in-production"
    )

    # ------------------------
    # Database
    # ------------------------
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(BASE_DIR, "instance", "app.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ------------------------
    # Project Paths
    # ------------------------
    REPORT_FOLDER = os.path.join(BASE_DIR, "reports")

    LOG_FOLDER = os.path.join(BASE_DIR, "logs")

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
