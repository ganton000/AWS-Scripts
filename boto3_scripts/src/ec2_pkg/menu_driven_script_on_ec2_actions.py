import boto3
import sys

profileName = 'default'

aws_mng_console = boto3.session.Session(profile_name=profileName)

ec2_con_res = aws_mng_console.resource(service_name='ec2', region_name='us-east-1')
ec2_con_cli = aws_mng_console.client(service_name='ec2', region_name='us-east-1')


def perform_action_on_ec2_instance_with_resource(res):
	while True:
		print("This script performs the following actions on an EC2 instance")
		print("""
		1. start
		2. stop
		3. terminate
		4. Exit
		""")
		opt = int(input('Enter your option: '))
		if opt == 1:
			instance_id=input('Enter your EC2 Instance Id :')
			instance_obj = res.Instance(instance_id)
			instance_obj.start()
			print("Starting EC2 Instance....")
		elif opt == 2:
			instance_id=input('Enter your EC2 Instance Id :')
			instance_obj = res.Instance(instance_id)
			instance_obj.stop()
			print("Stopping EC2 Instance....")
		elif opt == 3:
			instance_id=input('Enter your EC2 Instance Id :')
			instance_obj = res.Instance(instance_id)
			instance_obj.terminate()
			print("Terminating EC2 Instance....")
		elif opt == 4:
			print('Exiting... ')
			sys.exit()
		else:
			print("Your option is invalid.")

def perform_action_on_ec2_instance_with_client(client):
	while True:
		print("This script performs the following actions on an EC2 instance")
		print("""
		1. start
		2. stop
		3. terminate
		4. Exit
		""")
		opt = int(input('Enter your option: '))
		if opt == 1:
			instance_id=input('Enter your EC2 Instance Id :')
			client.start_instances(InstanceIds=[instance_id])
			print("Starting EC2 Instance....")
		elif opt == 2:
			instance_id=input('Enter your EC2 Instance Id :')
			client.stop_instances(InstanceIds=[instance_id])
			print("Stopping EC2 Instance....")
		elif opt == 3:
			instance_id=input('Enter your EC2 Instance Id :')
			client.terminate_instances(InstanceIds=[instance_id])
			print("Terminating EC2 Instance....")
		elif opt == 4:
			print('Exiting... ')
			sys.exit()
		else:
			print("Your option is invalid.")

#perform_action_on_ec2_instance_with_resource(ec2_con_res)
#perform_action_on_ec2_instance_with_client(ec2_con_cli)