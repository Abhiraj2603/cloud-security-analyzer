import boto3

from app.scanner.sg_scanner import (
    fetch_security_groups,
    fetch_network_interfaces,
    build_sg_usage_map,
    analyze_all,
    summarize,
)


class SGService:

    def __init__(self):
        self.session = boto3.Session()

    def scan(self):

        region = self.session.region_name or "us-east-1"

        sgs = fetch_security_groups(self.session, region)
        enis = fetch_network_interfaces(self.session, region)

        usage_map = build_sg_usage_map(enis)

        findings = analyze_all(
            sgs,
            usage_map,
            region
        )

        summary = summarize(
            findings,
            len(sgs),
            sum(
                1
                for sg in sgs
                if sg.get("GroupName") != "default"
                and not usage_map.get(
                    sg.get("GroupId"),
                    []
                )
            )
        )

        return {
            "summary": summary,
            "findings": findings,
            "security_groups": len(sgs),
            "region": region,
        }
