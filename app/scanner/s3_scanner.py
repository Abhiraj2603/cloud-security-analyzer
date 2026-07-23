import boto3
from botocore.exceptions import ClientError


class S3Scanner:

    def __init__(self):
        self.s3 = boto3.client("s3")
        self.findings = []

    def scan(self):

        buckets = self.s3.list_buckets()["Buckets"]

        summary = {
            "total_buckets": len(buckets),
            "public_buckets": 0,
            "encrypted_buckets": 0,
            "versioning_enabled": 0,
            "logging_enabled": 0,
            "lifecycle_enabled": 0,
        }

        inventory = []

        for bucket in buckets:

            name = bucket["Name"]

            bucket_info = {
                "name": name,
                "encryption": False,
                "versioning": False,
                "logging": False,
                "lifecycle": False,
                "public": False,
            }

            # ------------------------
            # Encryption
            # ------------------------

            try:

                self.s3.get_bucket_encryption(Bucket=name)

                bucket_info["encryption"] = True
                summary["encrypted_buckets"] += 1

            except ClientError:

                self.findings.append({
                    "service": "S3",
                    "severity": "HIGH",
                    "category": "Encryption",
                    "title": f"{name} is not encrypted",
                    "detail": "Bucket encryption is disabled.",
                    "remediation": "Enable SSE-S3 or SSE-KMS.",
                    "resource": name
                })

            # ------------------------
            # Versioning
            # ------------------------

            version = self.s3.get_bucket_versioning(Bucket=name)

            if version.get("Status") == "Enabled":
                bucket_info["versioning"] = True
                summary["versioning_enabled"] += 1

            else:

                self.findings.append({
                    "service": "S3",
                    "severity": "MEDIUM",
                    "category": "Versioning",
                    "title": f"Versioning disabled for {name}",
                    "detail": "Bucket versioning is disabled.",
                    "remediation": "Enable versioning.",
                    "resource": name
                })

            # ------------------------
            # Logging
            # ------------------------

            logging = self.s3.get_bucket_logging(Bucket=name)

            if logging.get("LoggingEnabled"):

                bucket_info["logging"] = True
                summary["logging_enabled"] += 1

            else:

                self.findings.append({
                    "service": "S3",
                    "severity": "LOW",
                    "category": "Logging",
                    "title": f"Logging disabled for {name}",
                    "detail": "Access logging is disabled.",
                    "remediation": "Enable bucket logging.",
                    "resource": name
                })

            # ------------------------
            # Lifecycle
            # ------------------------

            try:

                self.s3.get_bucket_lifecycle_configuration(
                    Bucket=name
                )

                bucket_info["lifecycle"] = True
                summary["lifecycle_enabled"] += 1

            except ClientError:
                pass

            # ------------------------
            # Public Access Block
            # ------------------------

            try:

                block = self.s3.get_public_access_block(
                    Bucket=name
                )

                config = block["PublicAccessBlockConfiguration"]

                if not all(config.values()):

                    bucket_info["public"] = True

                    summary["public_buckets"] += 1

                    self.findings.append({

                        "service": "S3",

                        "severity": "CRITICAL",

                        "category": "Public Bucket",

                        "title": f"{name} allows public access",

                        "detail": "Public access block is disabled.",

                        "remediation": "Enable Block Public Access.",

                        "resource": name

                    })

            except ClientError:

                bucket_info["public"] = True

                summary["public_buckets"] += 1

            inventory.append(bucket_info)

        summary["total_findings"] = len(self.findings)

        return {
            "summary": summary,
            "inventory": inventory,
            "findings": self.findings,
        }
