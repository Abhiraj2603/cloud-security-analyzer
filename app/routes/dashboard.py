from flask import Blueprint

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def home():
    return "<h1>Cloud Security Analyzer is running successfully 🚀</h1>"
