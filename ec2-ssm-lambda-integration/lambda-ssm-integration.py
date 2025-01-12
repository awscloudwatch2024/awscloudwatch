import boto3
import time


ssm_client = boto3.client('ssm', region_name='us-east-1')


def lambda_handler(event, context):

    response = ssm_client.send_command(
        #InstanceIds=[target_instance_name],
        DocumentName='AWS-RunShellScript',
        Parameters={'commands': ['mkdir /home/ec2-user/test2']},
        Targets=[{'Key': 'tag:purpose', 'Values': ['youtube']}],
        TimeoutSeconds=3600,
        MaxConcurrency='50',
        MaxErrors='0',
        CloudWatchOutputConfig={
            'CloudWatchOutputEnabled': True,
            'CloudWatchLogGroupName' : 'ssm-commandline-invoke'
        }
    )

    command_id = response['Command']['CommandId']
    print(command_id)
    time.sleep(5)

    list_command_invocation = ssm_client.list_command_invocations(
        CommandId=command_id,
        Details=True
    )

    for invoc in list_command_invocation['CommandInvocations']:
        status = invoc['StatusDetails']
        instance_id = invoc['InstanceId']
        print(f"Instance ID: {instance_id} Status: {status}")
        if status == 'Success':
            print(f"Instance ID: {instance_id} Status: {status}")
            print("Command execution successful.")
            break

    
