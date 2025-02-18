# This file was produced by https://github.com/ai-1st/dotprompt and shouldn't be edited directly.

import boto3
import base64
from concurrent.futures import ThreadPoolExecutor
import json

def lambda_handler(event, context):
    logs = []
    impaired_instances = []

    def log(message):
        print(message)
        logs.append(message)

    log("Starting EC2 rescue workflow for impaired Windows instances")

    # Default PowerShell script
    default_script = r'''
    get-childitem -path "$env:EC2RESCUE_OFFLINE_DRIVE\Windows\System32\drivers\CrowdStrike\" -Include C-00000291*.sys -Recurse | foreach { $_.Delete()}
    '''

    # Get script from event or use default
    offline_script = event.get('OfflineScript', default_script)
    offline_script_encoded = base64.b64encode(offline_script.encode()).decode()

    # Get test instance ID
    test_instance_id = event.get('TestInstanceId', 'i-0f62223f986e61018')

    ec2_client = boto3.client('ec2')

    try:
        regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    except Exception as e:
        log(f"Error fetching regions: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps({'error': str(e), 'logs': logs})}

    def process_region(region):
        regional_logs = []
        regional_impaired_instances = []

        def regional_log(message):
            print(f"{region}: {message}")
            regional_logs.append(f"{region}: {message}")

        regional_log(f"Processing region {region}")

        try:
            ec2 = boto3.client('ec2', region_name=region)
            ssm = boto3.client('ssm', region_name=region)

            # Get Windows instances
            windows_instances = []
            paginator = ec2.get_paginator('describe_instances')
            for page in paginator.paginate(Filters=[{'Name': 'platform', 'Values': ['windows']}]):
                for reservation in page['Reservations']:
                    windows_instances.extend([i['InstanceId'] for i in reservation['Instances'] if i['State']['Name'] == 'running'])

            regional_log(f"Found {len(windows_instances)} running Windows instances")

            # Get impaired instances
            impaired_instances = []
            paginator = ec2.get_paginator('describe_instance_status')
            for page in paginator.paginate(InstanceIds=windows_instances):
                impaired_instances.extend([i['InstanceId'] for i in page['InstanceStatuses'] if i['InstanceStatus']['Status'] != 'ok'])

            regional_log(f"Found {len(impaired_instances)} impaired Windows instances")

            # Add test instance if it's in this region
            try:
                ec2.describe_instances(InstanceIds=[test_instance_id])
                impaired_instances.append(test_instance_id)
                regional_log(f"Added test instance {test_instance_id}")
            except ec2.exceptions.ClientError:
                pass

            # Execute SSM runbook for each impaired instance
            for instance_id in impaired_instances:
                try:
                    response = ssm.start_automation_execution(
                        DocumentName='AWSSupport-StartEC2RescueWorkflow',
                        Parameters={
                            'CreatePreEC2RescueBackup': ['True'],
                            'InstanceId': [instance_id],
                            'OfflineScript': [offline_script_encoded]
                        }
                    )
                    regional_log(f"Started EC2 rescue workflow for instance {instance_id}: {response['AutomationExecutionId']}")
                    regional_impaired_instances.append(instance_id)
                except Exception as e:
                    regional_log(f"Error starting EC2 rescue workflow for instance {instance_id}: {str(e)}")

        except Exception as e:
            regional_log(f"Error processing region: {str(e)}")

        return regional_logs, regional_impaired_instances

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_region, regions))

    for regional_logs, regional_impaired_instances in results:
        logs.extend(regional_logs)
        impaired_instances.extend(regional_impaired_instances)

    log("Completed EC2 rescue workflow execution")

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'EC2 rescue workflow execution completed',
            'impaired_instances': impaired_instances,
            'logs': logs
        })
    }

if __name__ == "__main__":
    print(json.dumps(lambda_handler({}, None), indent=2))