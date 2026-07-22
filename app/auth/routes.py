from flask import Blueprint, render_template, request, redirect, session, url_for, flash

auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="../templates"
)

USERS = {
    "admin": {
        "password": "Admin@123",
        "role": "admin"
    },
    "auditor": {
        "password": "Audit@123",
        "role": "auditor"
    }
}


@auth_bp.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = USERS.get(username)

        if user and user["password"] == password:

            session["logged_in"] = True
            session["username"] = username
            session["role"] = user["role"]

            return redirect("/dashboard")

        flash("Invalid Username or Password")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/")
