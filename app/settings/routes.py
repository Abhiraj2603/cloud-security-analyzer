from flask import Blueprint, render_template, session, redirect, url_for
from datetime import datetime

settings_bp = Blueprint(
    "settings",
    __name__,
    template_folder="../templates"
)


@settings_bp.route("/settings")
def settings():

    if not session.get("logged_in"):
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        return redirect(url_for("dashboard.dashboard"))

    return render_template(
        "settings/settings.html",
        username=session.get("username"),
        role=session.get("role"),
        aws_region="ap-south-1",
        version="1.0",
        last_updated=datetime.now().strftime("%d %b %Y %I:%M %p")
    )
