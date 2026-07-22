from flask import Blueprint, jsonify

from app.services.scanner_service import run_scan

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/scan", methods=["POST"])
def scan():
    """
    Execute the AWS Security Group scan.
    """

    result = run_scan()

    if not result["success"]:
        return jsonify(result), 500

    return jsonify(result)
