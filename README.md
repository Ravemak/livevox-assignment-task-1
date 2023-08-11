# AWS Auto Scaling Group Verification

## Introduction

This Python project is intended to validate the specified test cases for an AWS Auto Scaling Group (ASG). The project covers two test cases: Test Case A and Test Case B. It uses Boto3 to interact with AWS services and perform the verifications.

### Test Case A

1. Verifies that the desired capacity matches the number of running instances.
2. Checks if multiple instances are distributed across multiple availability zones.
3. Ensures that Security Group, Image ID, and VPC ID match for all instances.
4. Identifies the instance with the longest uptime.

### Test Case B

1. Finds the next scheduled action for the ASG and calculates the time remaining.
2. Calculates the total number of instances launched and terminated on the current day for the given ASG.

## Credentials

This project uses AWS credentials for authentication. have set the following environment variables:

- `AWS_ACCESS_KEY_ID`: Your AWS access key ID
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key
