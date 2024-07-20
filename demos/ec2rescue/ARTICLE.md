# Automating Recovery of Windows Machines Affected by CrowdStrike Failure

On July 18th, 2024, a significant event occurred that impacted Windows-based devices across the globe. An update to the CrowdStrike Falcon agent (csagent.sys) caused unplanned stop errors or blue screens on affected machines. This incident didn't discriminate – it hit both on-premises systems and cloud-based resources, including Amazon EC2 instances and Amazon WorkSpaces Personal virtual desktops.

As an AWS user, you might have found yourself in a challenging situation, unable to connect to your resources. While a simple reboot often resolved the issue, some cases required more intricate solutions. That's where our automated recovery process comes in.

## The Challenge

Imagine waking up to find your entire fleet of Windows EC2 instances unresponsive. Your first instinct might be to manually recover each instance, a time-consuming and error-prone process. But what if there was a way to automate this recovery across all affected instances, regardless of their region?

## The Solution

We've developed a Lambda function that automates the execution of the AWSSupport-StartEC2RescueWorkflow SSM runbook on affected Windows EC2 instances. This solution, available on our [GitHub repository](https://github.com/ai-1st/dotprompt/blob/main/demos/ec2rescue), offers a streamlined approach to recovering from the CrowdStrike Falcon content update issue.

### How It Works

1. **Region Scanning**: The Lambda function first fetches a list of all active AWS EC2 regions. This ensures that no affected instance is left behind, regardless of its geographical location.

2. **Instance Identification**: For each region, the function identifies running Windows EC2 instances with a status of 'ok' or 'impaired'. This step is crucial as it allows us to target only the instances that need attention.

3. **Runbook Execution**: The function then executes the AWSSupport-StartEC2RescueWorkflow SSM runbook on each affected instance. This runbook is a powerful tool provided by AWS to automate instance recovery.

4. **Driver Removal**: As part of the recovery process, the function runs a PowerShell script to remove the specific driver file causing the issue. This step is key to preventing the problem from recurring after recovery.

## Deployment Made Easy

We've simplified the deployment process using AWS CloudFormation. With just a few CLI commands, you can have this solution up and running in your AWS environment. Here's how:

```bash
aws cloudformation create-stack --stack-name EC2RescueWorkflowStack --template-body file://cf.yaml --capabilities CAPABILITY_IAM
```

This command creates a new stack with all the necessary resources, including the Lambda function and required IAM roles.

## Executing the Recovery

Once deployed, you can trigger the recovery process with a simple Lambda invocation:

```bash
aws lambda invoke --function-name EC2RescueWorkflowLambda --payload '{}' output.json
```

This command executes the Lambda function, which then orchestrates the recovery process across all affected instances.

## Monitoring and Security

We understand the importance of visibility and security when it comes to automated processes. That's why our solution integrates with CloudWatch for logging and monitoring. You can track the progress of the recovery process and troubleshoot any issues that might arise.

Security is also a top priority. The Lambda function is granted only the necessary permissions to perform its tasks, adhering to the principle of least privilege.

## Conclusion

The CrowdStrike Falcon agent update issue was a stark reminder of how quickly things can go wrong in our interconnected world. However, it also presented an opportunity to showcase the power of automation in disaster recovery.

Our solution demonstrates how, with a bit of ingenuity and AWS's robust set of tools, we can turn a potential crisis into a manageable event. By automating the recovery process, we not only save time and reduce human error but also ensure a consistent approach across our entire infrastructure.

Remember, while this solution is tailored for the CrowdStrike issue, the principles behind it can be applied to various other scenarios. It's a testament to the flexibility and power of cloud computing and automation.

For more details and to implement this solution in your environment, visit our [GitHub repository](https://github.com/ai-1st/dotprompt/blob/main/demos/ec2rescue). Let's embrace automation and be better prepared for whatever challenges the future might bring!

---

*This article is based on a real-world scenario and solution. Always ensure you understand the actions performed by any automation scripts before running them in your environment. Test thoroughly in a non-production setting before applying to critical systems. For more information on the CrowdStrike Falcon agent issue and AWS's official guidance, refer to the [AWS Knowledge Center article](https://repost.aws/en/knowledge-center/ec2-instance-crowdstrike-agent).*