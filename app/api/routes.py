from flask import Blueprint, jsonify

from app.services.scanner_service import run_scan
from app.services.ai_service import generate_ai_summary

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/scan", methods=["POST"])
def scan():
    """
    Execute the AWS security scan and generate an AI security assessment.
    """

    result = run_scan()

    if not result["success"]:
        return jsonify(result), 500

    # Generate AI Summary using Ollama
    ai_summary = generate_ai_summary(result["data"])

    # Add AI summary to the response
    result["data"]["ai_summary"] = ai_summary

    return jsonify(result)
