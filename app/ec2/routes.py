from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
)

ec2_bp = Blueprint(
    "ec2",
    __name__,
    template_folder="../templates",
)


def login_required():
    return session.get("logged_in") is True


@ec2_bp.route("/ec2")
def ec2():

    if not login_required():
        return redirect(url_for("auth.login"))

    return render_template(
        "ec2/ec2.html",
        username=session.get("username"),
        role=session.get("role"),
    )
