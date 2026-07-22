from flask import Blueprint, session, redirect, url_for, abort, render_template

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
        abort(403)

    return render_template("settings/settings.html")
