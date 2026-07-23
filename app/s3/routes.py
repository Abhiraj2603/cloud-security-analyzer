from flask import Blueprint, render_template

s3_bp = Blueprint(
    "s3",
    __name__,
    url_prefix="/s3"
)

@s3_bp.route("/")
def index():
    return render_template("s3/s3.html")
