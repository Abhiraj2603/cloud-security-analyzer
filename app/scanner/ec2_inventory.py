import boto3


class EC2Inventory:

    def __init__(self):
        self.session = boto3.Session()
        self.ec2 = self.session.client("ec2")

    def get_instances(self):

        paginator = self.ec2.get_paginator("describe_instances")

        inventory = []

        for page in paginator.paginate():

            for reservation in page["Reservations"]:

                for instance in reservation["Instances"]:

                    tags = {
                        tag["Key"]: tag["Value"]
                        for tag in instance.get("Tags", [])
                    }

                    inventory.append({

                        "name": tags.get("Name", "-"),

                        "instance_id": instance["InstanceId"],

                        "state": instance["State"]["Name"],

                        "instance_type": instance["InstanceType"],

                        "private_ip":
                            instance.get("PrivateIpAddress", "-"),

                        "public_ip":
                            instance.get("PublicIpAddress", "-"),

                        "iam_role":
                            "Yes"
                            if "IamInstanceProfile" in instance
                            else "No",

                        "vpc_id":
                            instance.get("VpcId", "-"),

                        "subnet_id":
                            instance.get("SubnetId", "-"),

                        "availability_zone":
                            instance["Placement"]["AvailabilityZone"],

                        "architecture":
                            instance.get("Architecture", "-"),

                        "platform":
                            instance.get("Platform", "Linux"),

                        "launch_time":
                            instance["LaunchTime"].strftime(
                                "%Y-%m-%d %H:%M"
                            ),

                        "region":
                            self.ec2.meta.region_name,

                    })

        return inventory
