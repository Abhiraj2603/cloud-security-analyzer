import boto3


class EC2Scanner:

    def __init__(self):
        self.session = boto3.Session()
        self.ec2 = self.session.client("ec2")
        self.findings = []

    def scan(self):
        paginator = self.ec2.get_paginator("describe_instances")

        instances_found = 0

        for page in paginator.paginate():
            for reservation in page["Reservations"]:
                for instance in reservation["Instances"]:
                    instances_found += 1

                    print("=" * 60)
                    print("Instance ID :", instance["InstanceId"])
                    print("State       :", instance["State"]["Name"])
                    print("Public IP   :", instance.get("PublicIpAddress"))
                    print("IAM Role    :", "IamInstanceProfile" in instance)
                    print("Tags        :", instance.get("Tags", []))

                    self.check_public_ip(instance)
                    self.check_missing_name_tag(instance)
                    self.check_missing_iam_role(instance)

        print(f"\nInstances Found: {instances_found}")
        print(f"Findings Found : {len(self.findings)}")

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
