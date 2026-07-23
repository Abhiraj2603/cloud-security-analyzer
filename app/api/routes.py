from flask import Blueprint, jsonify

from app.services.scanner_service import run_scan
from app.services.sg_service import SGService
from app.services.iam_service import IAMService
from app.services.s3_service import S3Service
from app.scanner.ec2_inventory import EC2Inventory

api_bp = Blueprint("api", __name__)


# ==========================================================
# Run Complete Security Scan
# ==========================================================
@api_bp.route("/scan", methods=["POST"])
def scan():

    result = run_scan()

    if result["success"]:
        return jsonify(result["data"])

    return jsonify(result), 500


# ==========================================================
# EC2 Inventory
# ==========================================================
@api_bp.route("/ec2", methods=["GET"])
def ec2_inventory():

    inventory = EC2Inventory()

    return jsonify({
        "instances": inventory.get_inventory()
    })


# ==========================================================
# Security Groups
# ==========================================================
@api_bp.route("/security-groups", methods=["GET"])
def security_groups():

    service = SGService()

    data = service.scan()

    summary = data.get("summary", {})

    return jsonify({
        "summary": {
            "total_sgs": summary.get("total_sgs", 0),
            "total_findings": summary.get("total_findings", 0),
            "unused_sgs": summary.get("unused_sgs", 0),
            "CRITICAL": summary.get("CRITICAL", 0),
            "HIGH": summary.get("HIGH", 0),
            "MEDIUM": summary.get("MEDIUM", 0),
            "LOW": summary.get("LOW", 0),
        },
        "findings": data.get("findings", [])
    })


# ==========================================================
# IAM
# ==========================================================
@api_bp.route("/iam", methods=["GET"])
def iam():

    service = IAMService()

    return jsonify(service.scan())


# ==========================================================
# S3
# ==========================================================
@api_bp.route("/s3", methods=["GET"])
def s3():

    service = S3Service()

    return jsonify(service.scan())
