import boto3
import os
from dotenv import load_dotenv

load_dotenv()

access_key = os.environ.get("ACCESS_KEY")
secret_key = os.environ.get("SECRET_KEY")

def lambda_handler(event, context):
	session = boto3.session.Session(
		aws_access_key_id=access_key,
		aws_secret_access_key=secret_key)
	ec2_con = session.resource(service_name="ec2", region_name="us-east-1")

	for instance in ec2_con.instances.all():
		print(instance.id)

def autostart_test_ec2_instances_8am(event, context):
	'''
	EC2 Role is assigned to the lambda handler for session
	'''
	ec2_con_res = boto3.resource(service_name="ec2", region_name="us-east-1")

	test_env_filter = {
		"Name": "tag:Env",
		"Values": ["Test"]
	}
	for instance in ec2_con_res.instances.filter(Filters=[test_env_filter]):
		instance.start()

	return "Success"