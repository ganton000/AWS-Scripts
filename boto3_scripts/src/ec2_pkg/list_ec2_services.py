import boto3

#set iam user profile name
profileName = 'default'

#initialize client cli
aws_manage_console = boto3.session.Session(profile_name=profileName)
ec2_cli = aws_manage_console.client(service_name='ec2', region_name='us-east-1')

def get_ec2_instances_info(cli):
	instance_list = cli.describe_instances()['Reservations']

	if (len(instance_list) == 0):
		return print('No EC2 Instance Available')

	for each_item in instance_list:
		for instance in each_item['Instances']:
			print("===========================")
			print(f"The Image Id is: {instance['ImageId']}\n The Instance Id is: {instance['InstanceId']}\n The Instance Launch Time is: {instance['LaunchTime'].strftime('%Y-%m-%d')}")

#get_ec2_instances_info(ec2_cli)

def get_ec2_volumes_info(cli):
	volume_list = cli.describe_volumes()['Volumes']

	if (len(volume_list) == 0):
		return print('No EC2 Volume Available')

	for volume in volume_list:
		print("===========================")
		print(f"The Volume Id is: {volume['VolumeId']}\n The Availability Zone is: {volume['AvailabilityZone']}\n The Volume Type is: {volume['VolumeType']} The Volume Creation Time is: {volume['CreateTime'].strftime('%Y-%m-%d')}")

get_ec2_volumes_info(ec2_cli)