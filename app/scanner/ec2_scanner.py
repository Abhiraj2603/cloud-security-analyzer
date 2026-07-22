import boto3


class EC2Scanner:

    def __init__(self):
        self.session = boto3.Session(region_name="us-east-1")
        self.ec2 = self.session.client("ec2")
        self.ec2 = self.session.client("ec2")
        self.findings = []

    def scan(self):
        paginator = self.ec2.get_paginator("describe_instances")

        for page in paginator.paginate():
            for reservation in page["Reservations"]:
                for instance in reservation["Instances"]:
                    self.check_public_ip(instance)
                    self.check_missing_name_tag(instance)
                    self.check_missing_iam_role(instance)

        return self.findings

    def add_finding(
        self,
        instance,
        severity,
        category,
        title,
        detail,
        remediation,
    ):

        tags = {
            tag["Key"]: tag["Value"]
            for tag in instance.get("Tags", [])
        }

        self.findings.append(
            {
                "region": self.ec2.meta.region_name,
                "resource_id": instance["InstanceId"],
                "sg_name": tags.get("Name", instance["InstanceId"]),
                "severity": severity,
                "category": category,
                "title": title,
                "detail": detail,
                "remediation": remediation,
            }
        )

    def check_public_ip(self, instance):

        if instance.get("PublicIpAddress"):

            self.add_finding(
                instance,
                "MEDIUM",
                "EC2",
                "Public IP Address",
                f"Instance {instance['InstanceId']} has a public IP.",
                "Move the instance into a private subnet if public access is not required.",
            )

    def check_missing_name_tag(self, instance):

        tags = {
            tag["Key"]: tag["Value"]
            for tag in instance.get("Tags", [])
        }

        if "Name" not in tags:

            self.add_finding(
                instance,
                "LOW",
                "EC2",
                "Missing Name Tag",
                f"Instance {instance['InstanceId']} has no Name tag.",
                "Apply a Name tag for easier management.",
            )

    def check_missing_iam_role(self, instance):

        if "IamInstanceProfile" not in instance:

            self.add_finding(
                instance,
                "MEDIUM",
                "IAM",
                "No IAM Role Attached",
                f"Instance {instance['InstanceId']} has no IAM role.",
                "Attach an IAM Instance Profile.",
            )
