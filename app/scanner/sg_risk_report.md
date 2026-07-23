# AWS Security Group Risk Report

Generated: 2026-07-23 11:33 UTC
Account: 459858401338
Regions scanned: ap-south-1

## Summary

- **Security groups analyzed:** 2
- **Total findings:** 6
  - LOW: 6
- **Apparently unused security groups:** 0

## Findings

### ap-south-1 — sg-0bebad4742df69061 (default)

**[LOW] Unrestricted outbound access (all ports/protocols to 0.0.0.0/0)**  
*Category:* Unrestricted egress  
*Detail:* This is the AWS default egress rule. A compromised instance in this SG can freely exfiltrate data or reach any host.  
*Remediation:* Consider scoping egress to required destinations/ports for sensitive workloads.

**[LOW] No tags applied**  
*Category:* Hygiene  
*Detail:* This security group has no tags, making ownership, environment, and purpose unclear.  
*Remediation:* Apply standard tags (Owner, Environment, Application) per your tagging policy.

### ap-south-1 — sg-0dfc74c7e5cf30866 (launch-wizard-1)

**[LOW] Web port open to the internet (TCP/80)**  
*Category:* Internet-facing web port  
*Detail:* Rule permits TCP/80 from 0.0.0.0/0. Common/expected for public web servers or load balancers — confirm this SG fronts a public resource.  
*Remediation:* If attached to internal resources, restrict the source. If public-facing, ensure a WAF and rate limiting are in place.

**[LOW] Web port open to the internet (TCP/443)**  
*Category:* Internet-facing web port  
*Detail:* Rule permits TCP/443 from 0.0.0.0/0. Common/expected for public web servers or load balancers — confirm this SG fronts a public resource.  
*Remediation:* If attached to internal resources, restrict the source. If public-facing, ensure a WAF and rate limiting are in place.

**[LOW] Unrestricted outbound access (all ports/protocols to 0.0.0.0/0)**  
*Category:* Unrestricted egress  
*Detail:* This is the AWS default egress rule. A compromised instance in this SG can freely exfiltrate data or reach any host.  
*Remediation:* Consider scoping egress to required destinations/ports for sensitive workloads.

**[LOW] No tags applied**  
*Category:* Hygiene  
*Detail:* This security group has no tags, making ownership, environment, and purpose unclear.  
*Remediation:* Apply standard tags (Owner, Environment, Application) per your tagging policy.
