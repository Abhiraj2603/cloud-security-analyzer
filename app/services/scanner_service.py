import json
import os
import subprocess
import sys

from app.scanner.iam_scanner import IAMScanner
from app.scanner.ec2_scanner import EC2Scanner


def run_scan():
    """
    Execute the AWS Security Group, IAM and EC2 scanners
    and merge all findings.
    """

    scanner = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "scanner",
            "sg_scanner.py",
        )
    )

    output_file = "/tmp/aws_scan.json"

    cmd = [
        sys.executable,
        scanner,
        "--json",
        output_file,
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=os.path.dirname(scanner),
    )

    if result.returncode != 0:
        return {
            "success": False,
            "error": result.stderr,
            "stdout": result.stdout,
        }

    if not os.path.exists(output_file):
        return {
            "success": False,
            "error": "Scanner did not generate JSON.",
        }

    with open(output_file) as f:
        data = json.load(f)

    if "findings" not in data:
        data["findings"] = []

    # -------------------------------
    # IAM Scanner
    # -------------------------------

    try:

        iam_scanner = IAMScanner()

        iam_findings = iam_scanner.scan()

        if iam_findings:

            data["findings"].extend(iam_findings)

    except Exception as e:

        print(f"IAM Scanner Error: {e}")

    # -------------------------------
    # EC2 Scanner
    # -------------------------------

    try:

        ec2_scanner = EC2Scanner()

        ec2_findings = ec2_scanner.scan()

        if ec2_findings:

            data["findings"].extend(ec2_findings)

    except Exception as e:

        print(f"EC2 Scanner Error: {e}")

    # -------------------------------
    # Update Summary
    # -------------------------------

    summary = data.get("summary", {})

    summary["total_findings"] = len(data["findings"])

    summary["CRITICAL"] = len(
        [f for f in data["findings"] if f["severity"] == "CRITICAL"]
    )

    summary["HIGH"] = len(
        [f for f in data["findings"] if f["severity"] == "HIGH"]
    )

    summary["MEDIUM"] = len(
        [f for f in data["findings"] if f["severity"] == "MEDIUM"]
    )

    summary["LOW"] = len(
        [f for f in data["findings"] if f["severity"] == "LOW"]
    )

    data["summary"] = summary

    return {
        "success": True,
        "data": data,
    }
