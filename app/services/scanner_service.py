import json
import os
import subprocess
import sys


def run_scan():
    """
    Execute the AWS Security Group scanner.
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
        sys.executable,          # Use the same Python interpreter as Flask
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

    return {
        "success": True,
        "data": data,
    }
