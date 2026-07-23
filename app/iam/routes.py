from flask import Blueprint, render_template

iam_bp = Blueprint(
    "iam",
    __name__,
    url_prefix="/iam"
)


@iam_bp.route("/")
def index():
    return render_template("iam/iam.html")
