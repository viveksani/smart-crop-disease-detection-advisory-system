# AWS Deployment Status

## Prepared

- CloudFormation stack for EC2, S3, DynamoDB, IAM, and CloudWatch.
- Dockerized Flask application with the trained model and label file.
- PowerShell deployment and cleanup scripts.
- HTTP access is restricted by a required IPv4 CIDR allowlist; the deploy script rejects `0.0.0.0/0`.

## Not yet deployed

No AWS resources were created from this workspace. The computer currently has no AWS CLI installation, no configured AWS credentials/profile files, and no signed-in AWS console browser session. Deployment therefore needs the account owner to authenticate through the college or account's approved AWS workflow first. Do not paste access keys or session tokens into chat.

## Deployment steps after AWS authentication

1. Install AWS CLI v2 and sign in with the AWS account/profile that owns the project.
2. Choose the IPv4 CIDR allowed to reach the demo, such as a reviewer or office egress IP with `/32`.
3. Run `scripts/deploy.ps1` with the selected AWS profile, region, and CIDR. The default region is `ap-south-1`.
4. Wait for `/healthz` to report the app is ready, then verify image upload, prediction display, S3 storage, and DynamoDB history.
5. Capture AWS console and application screenshots for the college submission.

The stack creates billable resources. Review the CloudFormation stack and its outputs in the account, and remove it with `scripts/destroy.ps1` when the demo is no longer needed.
