# Automating Recovery of Windows EC2 Instances Affected by CrowdStrike Failure

On July 18th, 2024, a significant event occurred that affected many Windows-based AWS resources. An update to the CrowdStrike Falcon agent (csagent.sys) caused Windows-based devices, including Amazon EC2 instances and Amazon WorkSpaces, to experience unplanned stop errors or blue screens. This incident left many system administrators scrambling to recover their affected resources.

In this article, we'll explore an automated solution to recover these impaired Windows EC2 instances efficiently and at scale. We'll dive into a Lambda function that leverages the AWS Systems Manager automation runbook to streamline the recovery process.

## The Challenge

The CrowdStrike Falcon agent update issue affected a large number of Windows EC2 instances across multiple AWS regions. While a simple reboot resolved the problem for some instances, many remained in an impaired state, requiring more extensive intervention.

Manually recovering these instances would be a time-consuming and error-prone process, especially for organizations managing a large fleet of EC2 instances across multiple regions.

## The Solution

To address this challenge, we've developed a Lambda function that automates the recovery process using the `AWSSupport-StartEC2RescueWorkflow` Systems Manager automation runbook. This solution can be found in our GitHub repository: [EC2 Rescue Workflow Lambda Function](https://github.com/ai-1st/dotprompt/blob/main/demos/ec2rescue).

Here's how the Lambda function works:

1. It fetches a list of all active AWS EC2 regions.
2. For each region, it identifies running Windows EC2 instances.
3. It then identifies impaired instances and includes a test instance if specified.
4. The function executes the `AWSSupport-StartEC2RescueWorkflow` SSM runbook for each impaired instance.
5. Finally, it logs the process and returns the results.

## Key Features

1. **Multi-Region Support**: The function operates across all active EC2 regions, ensuring comprehensive coverage of your AWS infrastructure.

2. **Automated Instance Identification**: It automatically identifies impaired Windows instances, reducing the need for manual intervention.

3. **Scalability**: The solution can handle recovery for multiple instances across various regions simultaneously.

4. **Customization**: You can specify a test instance ID and provide a custom offline script for more tailored recovery processes.

5. **Logging and Reporting**: The function logs its actions and provides a detailed report of the recovery process.

## Deployment and Usage

The solution is packaged as a CloudFormation template, making it easy to deploy in your AWS environment. Here's a quick overview of the deployment process:

1. Save the CloudFormation template to a file named `cf.yaml`.
2. Use the AWS CLI to create the stack:

```bash
aws cloudformation create-stack --stack-name EC2RescueWorkflowStack --template-body file://cf.yaml --capabilities CAPABILITY_IAM
```

3. Once deployed, you can invoke the Lambda function with a JSON payload specifying any test instances and custom offline scripts.

For detailed deployment instructions and usage guidelines, please refer to the README in our [GitHub repository](https://github.com/ai-1st/dotprompt/blob/main/demos/ec2rescue).

## The Recovery Process

The Lambda function utilizes the `AWSSupport-StartEC2RescueWorkflow` Systems Manager automation runbook to perform the recovery. This runbook performs the following steps:

1. Launches a temporary EC2 instance (helper instance) in a VPC.
2. Mounts the root volume of the affected instance to the helper instance.
3. Runs a command to delete the problematic CrowdStrike file:

```powershell
get-childitem -path "$env:EC2RESCUE_OFFLINE_DRIVE\Windows\System32\drivers\CrowdStrike\" -Include C-00000291*.sys -Recurse | foreach { $_.Delete()}
```

4. Unmounts the volume and terminates the helper instance.

This process effectively removes the faulty CrowdStrike file without the need to manually access each affected instance.

## Considerations and Best Practices

While this automated solution can significantly speed up the recovery process, it's important to keep the following points in mind:

1. **Testing**: Always test the solution in a non-production environment before running it on production instances.

2. **Permissions**: The Lambda function requires administrative access. In a production environment, follow the principle of least privilege and grant only the necessary permissions.

3. **Encrypted Volumes**: If your EBS root volumes are encrypted, ensure that the encryption keys are accessible and that you have the necessary permissions.

4. **Instance Store Volumes**: Be aware that data on instance store volumes does not persist when an instance is stopped. If your instances use instance store volumes, consider using the manual recovery method instead.

5. **Monitoring**: Keep an eye on the CloudWatch Logs for the Lambda function to catch and address any issues that may arise during the recovery process.

## Conclusion

The CrowdStrike Falcon agent update issue of July 2024 served as a stark reminder of the importance of having robust, automated recovery processes in place. By leveraging AWS services like Lambda and Systems Manager, we can create powerful solutions that allow us to respond quickly and efficiently to such incidents.

The automated recovery solution presented here demonstrates how we can use AWS's native tools to build resilient systems that can recover from failures with minimal manual intervention. As cloud environments grow more complex, such automation becomes not just beneficial, but essential for maintaining system reliability and minimizing downtime.

For more information on the CrowdStrike issue and alternative recovery methods, you can refer to the [AWS knowledge center article](https://repost.aws/en/knowledge-center/ec2-instance-crowdstrike-agent).

Remember, in the world of cloud computing, automation is your best friend. It not only saves time but also reduces the risk of human error in critical recovery processes. Stay prepared, stay automated!