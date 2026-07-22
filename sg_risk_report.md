# AWS Security Group Risk Report

Generated: 2026-07-21 23:52 UTC
Account: 459858401338
Regions scanned: us-east-1

## Summary

- **Security groups analyzed:** 1
- **Total findings:** 2
  - LOW: 2
- **Apparently unused security groups:** 0

## Findings

### us-east-1 — sg-0484b2462ab743d6d (default)

**[LOW] Unrestricted outbound access (all ports/protocols to 0.0.0.0/0)**  
*Category:* Unrestricted egress  
*Detail:* This is the AWS default egress rule. A compromised instance in this SG can freely exfiltrate data or reach any host.  
*Remediation:* Consider scoping egress to required destinations/ports for sensitive workloads.

**[LOW] No tags applied**  
*Category:* Hygiene  
*Detail:* This security group has no tags, making ownership, environment, and purpose unclear.  
*Remediation:* Apply standard tags (Owner, Environment, Application) per your tagging policy.
