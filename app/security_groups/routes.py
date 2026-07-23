from flask import Blueprint, render_template

sg_bp = Blueprint(
    "security_groups",
    __name__,
    template_folder="../templates"
)


@sg_bp.route("/security-groups")
def security_groups():
    return render_template("security_groups/security_groups.html")
