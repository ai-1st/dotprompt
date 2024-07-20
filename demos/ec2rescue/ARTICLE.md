# Automated Recovery of Windows EC2 Instances Affected by CrowdStrike Failure

On July 18th, 2024, a significant event occurred that sent shockwaves through the AWS ecosystem. An update to the CrowdStrike Falcon agent (csagent.sys) caused Windows-based devices, including Amazon EC2 instances and WorkSpaces, to experience unplanned stop errors or blue screens. This incident left many system administrators scrambling to recover their affected resources.

In this article, we'll explore an automated solution to this problem, demonstrating how to leverage AWS Lambda and Systems Manager to efficiently recover impaired Windows EC2 instances across multiple regions.

## The Challenge

The CrowdStrike Falcon agent update affected numerous Windows EC2 instances, causing them to become unresponsive. While a simple reboot resolved the issue for some instances, others remained in an impaired state. Manual recovery processes were time-consuming and error-prone, especially for organizations managing large fleets of EC2 instances across multiple AWS regions.

## The Solution

To address this challenge, we've developed an automated solution using AWS Lambda and the AWSSupport-StartEC2RescueWorkflow Systems Manager automation runbook. This solution can identify impaired instances across all AWS regions and initiate the recovery process automatically.

The core of our solution is a Lambda function that performs the following tasks:

1. Fetches a list of all active AWS EC2 regions
2. Identifies running Windows EC2 instances in each region
3. Detects impaired instances (and optionally includes a test instance)
4. Executes the AWSSupport-StartEC2RescueWorkflow SSM runbook for each impaired instance
5. Logs the process and returns the results

You can find the complete implementation of this solution in our GitHub repository: [EC2 Rescue Workflow Lambda Function](https://github.com/ai-1st/dotprompt/blob/main/demos/ec2rescue)

## How It Works

The Lambda function leverages the AWS SDK to interact with EC2 and Systems Manager services across all regions. Here's a high-level overview of the process:

1. **Region Discovery**: The function starts by fetching a list of all active EC2 regions in your AWS account.

2. **Instance Identification**: For each region, it identifies running Windows EC2 instances.

3. **Impairment Detection**: The function then checks the status of each instance to determine if it's impaired. It also allows for the inclusion of a test instance if specified.

4. **Recovery Initiation**: For each impaired instance, the function initiates the AWSSupport-StartEC2RescueWorkflow SSM runbook. This runbook performs the following actions:
   - Stops the impaired instance
   - Launches a temporary helper instance
   - Attaches the impaired instance's root volume to the helper instance
   - Deletes the problematic CrowdStrike file
   - Reattaches the root volume to the original instance
   - Starts the recovered instance

5. **Logging and Reporting**: Throughout the process, the function logs its actions and ultimately returns a summary of the recovery operations.

## Deployment and Usage

To deploy this solution, you'll need to:

1. Save the CloudFormation template provided in the GitHub repository.
2. Use the AWS CLI or CloudFormation console to create a new stack using this template.
3. Once deployed, you can invoke the Lambda function manually or set up a trigger based on your needs.

For detailed deployment instructions and usage guidelines, please refer to the README in the GitHub repository.

## Benefits of This Approach

This automated solution offers several advantages over manual recovery methods:

1. **Speed**: It can rapidly identify and initiate recovery for impaired instances across all regions simultaneously.
2. **Consistency**: The automated process ensures that the same recovery steps are applied consistently to all affected instances.
3. **Scalability**: Whether you have 10 or 10,000 affected instances, this solution can handle the load.
4. **Reduced Human Error**: By automating the process, we minimize the risk of mistakes that can occur during manual recovery.
5. **Comprehensive Coverage**: The solution checks all regions, ensuring no affected instances are overlooked.

## Conclusion

The CrowdStrike Falcon agent update incident serves as a reminder of the importance of having robust, automated recovery processes in place. By leveraging AWS services like Lambda and Systems Manager, we can create powerful solutions that help us respond quickly and effectively to such incidents.

While this solution was developed in response to a specific event, the underlying principles and techniques can be adapted to address a wide range of EC2 instance recovery scenarios. As cloud environments grow increasingly complex, such automated solutions will become essential tools in every cloud administrator's toolkit.

For more information about the CrowdStrike incident and alternative recovery methods, you can refer to the [AWS knowledge center article](https://repost.aws/en/knowledge-center/ec2-instance-crowdstrike-agent).

Remember, in the world of cloud computing, automation is not just a convenience—it's a necessity. Stay prepared, stay automated, and keep your cloud resources running smoothly!