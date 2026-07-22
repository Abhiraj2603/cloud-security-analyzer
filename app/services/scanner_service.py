import json
import os
import subprocess
import sys

from app.scanner.iam_scanner import IAMScanner


def run_scan():
    """
    Execute the AWS Security Group scanner and IAM scanner,
    then merge the findings.
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
        sys.executable,  # Use the same Python interpreter as Flask
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

    # Ensure findings key exists
    if "findings" not in data:
        data["findings"] = []

    # Run IAM Scanner
    try:
        iam_scanner = IAMScanner()
        iam_findings = iam_scanner.scan()

        if iam_findings:
            data["findings"].extend(iam_findings)

    except Exception as e:
        print(f"IAM Scanner Error: {e}")

    return {
        "success": True,
        "data": data,
    }
