#make sure ec2 instance has a secondary private IP configured
#(right click - network -> manage IP)
#so secondary ip gets assigned to failover instance
#Also enable ec2 permissions for lambda role

##func name: AutoAssignSecondaryIPWhenEC2GoesDown
#execution role:

import json
import boto3

def get_instance_ip(instance_name: str) -> str:
	'''
	instance_name arg refers to value of tag with key "Name"
	'''
	ec2_client = boto3.client('ec2')
	response = ec2_client.describe_instances(Filters=[{
		'Name': 'tag:Name',
		'Values': [instance_name]
		}],InstanceIds=[])['Reservations'][0]
	instance = response['Instances'][0]
	ip_addresses = instance['NetworkInterfaces'][0]['PrivateIpAddresses']
	secondary_address = [ ip_address['PrivateIpAddress'] for ip_address in ip_addresses if ip_address['Primary'] != True ]
	return secondary_address[0]


#get_instance_ip('RedHat-Server')

def get_instance_id(instance_name: str) -> str:
	'''
	instance_name arg refers to value of tag with key "Name"
	'''
	ec2_client = boto3.client('ec2')
	response = ec2_client.describe_instances(Filters=[{
		'Name': 'tag:Name',
		'Values': [instance_name]
		}],InstanceIds=[])['Reservations'][0]
	return response['Instances'][0]['InstanceId']

def lambda_handler(event, context):
	original_instance_id= get_instance_id(orig_instance)
	failover_instance_id= get_instance_id(failover_instance)

	ec2_re = boto3.resource("ec2", "us-east-1")
	primary_instance = ec2_re.Instance(original_instance_id)

	if primary_instance.state['Name'] == "running":
		print("Primary instance is running, no need of any modifications")
	else:
		secondary_instance = ec2_re.Instance(failover_instance_id)

		#need to get networkInterfaceId to use assign/unassign private_ip client method
		primary_network_interface_info = primary_instance.network_interfaces_attribute[0]
		secondary_network_interface_info = primary_instance.network_interfaces_attribute[0]

		pnw_interface_id= primary_network_interface_info['NetworkInterfaceId']
		snw_interface_id= secondary_network_interface_info['NetworkInterfaceId']
		secondary_ip= get_instance_ip(orig_instance)

		ec2_client = boto3.client("ec2", "us-east-1")
		#unassign ip (can only be done in client)
		ec2_client.unassign_private_ip_addresses(
			NetworkInterfaceId=pnw_interface_id,
			PrivateIpAddresses=[secondary_ip]
		)

		#assign to new networkinterface (of secondary ec2 instance)
		ec2_client.assign_private_ip_addresses(
			AllowReassignment=True,
			NetworkInterfaceId=snw_interface_id,
			PrivateIpAddresses=[secondary_ip]
		)

	return None


orig_instance = "RedHat-Server"
failover_instance = "RedHat-Server2"