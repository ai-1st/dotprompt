# AWS Lambda Function for EC2 Rescue Workflow

This repository contains a Lambda function and CloudFormation template to automate the execution of the AWSSupport-StartEC2RescueWorkflow SSM runbook on Windows EC2 instances affected by the CrowdStrike Falcon content update issue.

## Overview

The Lambda function performs the following tasks:

1. Fetches a list of all active AWS EC2 regions
2. For each region, retrieves running Windows EC2 instances with status 'ok' or 'impaired'
3. Executes the AWSSupport-StartEC2RescueWorkflow SSM runbook on each affected instance
4. Runs a PowerShell script to remove a specific driver file causing the issue

## Prerequisites

- AWS CLI installed and configured with appropriate permissions
- Python 3.8 or later

## Deployment

### Initial Deployment

To deploy the CloudFormation stack using the AWS CLI, run the following command:

```bash
aws cloudformation create-stack --stack-name EC2RescueWorkflowStack --template-body file://cf.yaml --capabilities CAPABILITY_IAM
```

### Redeployment

To update an existing stack, use the following command:

```bash
aws cloudformation update-stack --stack-name EC2RescueWorkflowStack --template-body file://cf.yaml --capabilities CAPABILITY_IAM
```

## Running the Lambda Function

To invoke the Lambda function using the AWS CLI, use the following command:

```bash
aws lambda invoke --function-name EC2RescueWorkflowLambda --payload '{}' output.json
```

This will execute the Lambda function with default parameters. The output will be stored in `output.json`.

To provide a custom PowerShell script, you can pass it as part of the payload:

```bash
aws lambda invoke --function-name EC2RescueWorkflowLambda --payload '{"OfflineScript": "Your custom PowerShell script here"}' output.json
```

## Monitoring

You can monitor the execution of the Lambda function and the SSM Automation executions in the AWS Management Console:

1. Check the CloudWatch Logs for the Lambda function to see detailed execution logs.
2. Visit the AWS Systems Manager Automation console to view the status of individual SSM Automation executions.

## Security Considerations

- The Lambda function is granted permissions to describe EC2 instances and regions, and to start SSM Automation executions.
- Ensure that your AWS account has the necessary permissions to run the AWSSupport-StartEC2RescueWorkflow SSM runbook.
- Review and adjust the IAM roles and policies as needed for your specific security requirements.

## Troubleshooting

- If you encounter permission issues, verify that the Lambda execution role has the necessary permissions.
- For any errors during execution, check the CloudWatch Logs for the Lambda function for detailed error messages.

## Disclaimer

This solution is provided as-is. Always test in a non-production environment before running in production. Ensure you understand the actions performed by the SSM runbook and the PowerShell script before execution.