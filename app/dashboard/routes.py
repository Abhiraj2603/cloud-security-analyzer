from flask import (
    Blueprint,
    render_template,
    send_file,
    session,
    redirect,
    url_for,
)

from app.services.scanner_service import run_scan
from app.services.pdf_service import PDFService
from app.services.excel_service import generate_excel

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    template_folder="../templates"
)


def login_required():
    return session.get("logged_in") is True


@dashboard_bp.route("/dashboard")
def dashboard():

    if not login_required():
        return redirect(url_for("auth.login"))

    return render_template(
        "dashboard/dashboard.html",
        username=session.get("username"),
        role=session.get("role")
    )


@dashboard_bp.route("/download/pdf")
def download_pdf():

    if not login_required():
        return redirect(url_for("auth.login"))

    result = run_scan()

    if not result["success"]:
        return "Scan Failed", 500

    pdf = PDFService.generate_report(result["data"])

    return send_file(
        pdf,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="Cloud_Security_Report.pdf",
    )


@dashboard_bp.route("/download/excel")
def download_excel():

    if not login_required():
        return redirect(url_for("auth.login"))

    result = run_scan()

    if not result["success"]:
        return "Scan Failed", 500

    excel = generate_excel(result["data"])

    return send_file(
        excel,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="Cloud_Security_Report.xlsx",
    )
