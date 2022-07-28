'''
Make sure this lambda function has attached iam role
with permissions to EC2 and SNS

funcName (example): MailAlertForProdServers

For SNS usage, create an SNS Topic to use

Create CloudWatch rule to trigger this Lambda Function
depending on state of EC2 (in this case, EC2 stopped)
1. Events -> Rule -> Event Pattern:
	Service Name: EC2
	Event Type: Instance State-change Notification
	Specific State(s): Stopped
	Specific Instance Id(s) or Any
2. Add Target -> Lambda Function
3. Configure Details, give Rule name/description
4. Create Rule
'''

import json
import boto3


def lambda_handler(event_context):
	ec2_console = boto3.resource("ec2", "us-east-1")
	sns_client = boto3.client("sns")

	instance_id = "some instance id"
	sns_topic_arn = "some arn"

	my_instance= ec2_console.Instance(instance_id)

	sns_client.publish(
		TargetArn= sns_topic_arn,
		Message= my_instance.state['Name']
		)