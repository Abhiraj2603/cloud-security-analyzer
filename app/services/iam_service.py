import boto3

from app.scanner.iam_scanner import IAMScanner


class IAMService:
    """
    Service responsible for collecting IAM inventory
    and security findings.
    """

    def __init__(self):
        self.session = boto3.Session()
        self.iam = self.session.client("iam")

    def scan(self):

        scanner = IAMScanner()
        findings = scanner.scan()

        users = self.iam.list_users()["Users"]
        roles = self.iam.list_roles()["Roles"]
        groups = self.iam.list_groups()["Groups"]

        total_users = len(users)
        total_roles = len(roles)
        total_groups = len(groups)

        mfa_disabled = 0
        admin_users = 0
        root_keys = 0
        old_access_keys = 0
        unused_users = 0

        summary = self.iam.get_account_summary()["SummaryMap"]

        if summary.get("AccountAccessKeysPresent", 0) > 0:
            root_keys = 1

        for user in users:

            username = user["UserName"]

            # MFA
            devices = self.iam.list_mfa_devices(
                UserName=username
            )["MFADevices"]

            if len(devices) == 0:
                mfa_disabled += 1

            # AdministratorAccess
            attached = self.iam.list_attached_user_policies(
                UserName=username
            )["AttachedPolicies"]

            for policy in attached:
                if policy["PolicyName"] == "AdministratorAccess":
                    admin_users += 1

            # Access Keys
            keys = self.iam.list_access_keys(
                UserName=username
            )["AccessKeyMetadata"]

            for key in keys:

                age = (
                    (
                        __import__("datetime").datetime.now(
                            key["CreateDate"].tzinfo
                        )
                        - key["CreateDate"]
                    ).days
                )

                if age > 90:
                    old_access_keys += 1

            # Console login

            try:

                last_used = self.iam.get_user(
                    UserName=username
                )["User"].get("PasswordLastUsed")

                if last_used is None:
                    unused_users += 1

            except Exception:
                pass

        severity = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
        }

        for finding in findings:

            sev = finding.get("severity", "").upper()

            if sev in severity:
                severity[sev] += 1

        return {
            "summary": {
                "total_users": total_users,
                "total_roles": total_roles,
                "total_groups": total_groups,
                "mfa_disabled": mfa_disabled,
                "admin_users": admin_users,
                "root_keys": root_keys,
                "old_access_keys": old_access_keys,
                "unused_users": unused_users,
                "total_findings": len(findings),
                "CRITICAL": severity["CRITICAL"],
                "HIGH": severity["HIGH"],
                "MEDIUM": severity["MEDIUM"],
                "LOW": severity["LOW"],
            },
            "findings": findings,
        }
