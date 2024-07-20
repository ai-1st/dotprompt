# EC2 Rescue Workflow Lambda Function

This repository contains a Lambda function and CloudFormation template designed to automate the process of rescuing impaired Windows EC2 instances affected by the CrowdStrike Falcon content update.

## Overview

The Lambda function performs the following tasks:

1. Fetches a list of all active AWS EC2 regions
2. For each region, identifies running Windows EC2 instances
3. Identifies impaired instances and includes a test instance if specified
4. Executes the `AWSSupport-StartEC2RescueWorkflow` SSM runbook for each impaired instance
5. Logs the process and returns the results

## Deployment Instructions

### Prerequisites

- AWS CLI installed and configured with appropriate permissions
- An AWS account with necessary permissions to create Lambda functions, IAM roles, and execute SSM runbooks

### Deploying the Stack

1. Save the CloudFormation template to a file named `cf.yaml`.

2. Open a terminal and navigate to the directory containing `cf.yaml`.

3. Run the following AWS CLI command to create the stack:

   ```
   aws cloudformation create-stack --stack-name EC2RescueWorkflowStack --template-body file://cf.yaml --capabilities CAPABILITY_IAM
   ```

4. Wait for the stack creation to complete. You can check the status using:

   ```
   aws cloudformation describe-stacks --stack-name EC2RescueWorkflowStack --query 'Stacks[0].StackStatus'
   ```

   Wait until the status is `CREATE_COMPLETE`.

### Redeploying the Stack

If you need to update the Lambda function or make changes to the stack:

1. Make your changes to the `cf.yaml` file.

2. Run the following AWS CLI command to update the stack:

   ```
   aws cloudformation update-stack --stack-name EC2RescueWorkflowStack --template-body file://cf.yaml --capabilities CAPABILITY_IAM
   ```

3. Wait for the update to complete, checking the status as before.

## Running the Lambda Function

To invoke the Lambda function:

1. Create a JSON file named `input.json` with the following content (customize as needed):

   ```json
   {
     "TestInstanceId": "i-0f62223f986e61018",
     "OfflineScript": "get-childitem -path \"$env:EC2RESCUE_OFFLINE_DRIVE\\Windows\\System32\\drivers\\CrowdStrike\\\" -Include C-00000291*.sys -Recurse | foreach { $_.Delete()}"
   }
   ```

2. Run the following AWS CLI command:

   ```
   aws lambda invoke --function-name EC2RescueWorkflowLambda --payload file://input.json output.json
   ```

3. The function's output will be saved in `output.json`. You can view it using:

   ```
   cat output.json
   ```

## Notes

- The Lambda function has a timeout of 900 seconds (15 minutes) and 256 MB of memory. Adjust these in the CloudFormation template if needed.
- The function uses the AdministratorAccess managed policy for simplicity. In a production environment, you should create a more restrictive custom policy.
- Always test in a non-production environment first before running in production.

## Security Considerations

- The Lambda function is granted administrative access. In a production environment, follow the principle of least privilege and grant only the necessary permissions.
- Ensure that your AWS account is properly secured and that access to the Lambda function is restricted to authorized personnel only.

## Troubleshooting

- If you encounter any issues, check the CloudWatch Logs for the Lambda function for detailed error messages and logs.
- Ensure that your AWS CLI is properly configured with the correct credentials and region.