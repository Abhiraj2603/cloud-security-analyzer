import boto3


class IAMScanner:

    def __init__(self):
        self.iam = boto3.client("iam")
        self.findings = []

    def scan(self):
        """
        Run all IAM security checks.
        """
        self.check_root_access_keys()
        self.check_users_without_mfa()
        self.check_admin_users()

        return self.findings

    # --------------------------------------------------
    # Root Access Keys
    # --------------------------------------------------

    def check_root_access_keys(self):

        summary = self.iam.get_account_summary()["SummaryMap"]

        if summary.get("AccountAccessKeysPresent", 0) > 0:

            self.findings.append({
                "service": "IAM",
                "severity": "CRITICAL",
                "category": "Root Account",
                "title": "Root account has active access keys",
                "detail": "Root access keys should not be used.",
                "remediation": "Delete the root access keys and use IAM users or IAM roles.",
                "resource": "Root Account"
            })

    # --------------------------------------------------
    # MFA Check
    # --------------------------------------------------

    def check_users_without_mfa(self):

        users = self.iam.list_users()["Users"]

        for user in users:

            devices = self.iam.list_mfa_devices(
                UserName=user["UserName"]
            )["MFADevices"]

            if len(devices) == 0:

                self.findings.append({

                    "service": "IAM",

                    "severity": "HIGH",

                    "category": "MFA",

                    "title": f"MFA not enabled for {user['UserName']}",

                    "detail": f"IAM user {user['UserName']} does not have MFA enabled.",

                    "remediation": "Enable MFA for this IAM user.",

                    "resource": user["UserName"]

                })

    # --------------------------------------------------
    # AdministratorAccess
    # --------------------------------------------------

    def check_admin_users(self):

        users = self.iam.list_users()["Users"]

        for user in users:

            attached = self.iam.list_attached_user_policies(
                UserName=user["UserName"]
            )["AttachedPolicies"]

            for policy in attached:

                if policy["PolicyName"] == "AdministratorAccess":

                    self.findings.append({

                        "service": "IAM",

                        "severity": "HIGH",

                        "category": "Administrator Access",

                        "title": f"{user['UserName']} has AdministratorAccess",

                        "detail": "User has full administrative permissions.",

                        "remediation": "Grant least-privilege permissions instead of full administrator access.",

                        "resource": user["UserName"]

                    })
