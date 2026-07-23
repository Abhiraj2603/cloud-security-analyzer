from app.scanner.s3_scanner import S3Scanner


class S3Service:
    """
    Service layer for S3 Security.
    Calls the scanner and prepares the
    data for the REST API.
    """

    def __init__(self):
        self.scanner = S3Scanner()

    def scan(self):

        result = self.scanner.scan()

        summary = result.get("summary", {})
        findings = result.get("findings", [])
        inventory = result.get("inventory", [])

        severity = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
        }

        for finding in findings:

            level = finding.get("severity", "").upper()

            if level in severity:
                severity[level] += 1

        summary["CRITICAL"] = severity["CRITICAL"]
        summary["HIGH"] = severity["HIGH"]
        summary["MEDIUM"] = severity["MEDIUM"]
        summary["LOW"] = severity["LOW"]

        return {
            "summary": summary,
            "inventory": inventory,
            "findings": findings,
        }
