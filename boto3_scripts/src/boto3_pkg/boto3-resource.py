import boto3

aws_manage_console = boto3.session.Session(profile_name='default')

iam_console_cli = aws_manage_console.resource(service_name='iam', region_name='us-east-1')
ec2_console_cli = aws_manage_console.resource(service_name='ec2', region_name='us-east-1')
s3_console_cli = aws_manage_console.resource(service_name='s3', region_name='us-east-1')

def get_and_print_iam_users(resource):
	response = resource.users.all() #returns iterable
	for each_item in response:
		print(each_item.user_name) #dir() shows attributes

#get_and_print_iam_users(iam_console_cli)

def get_and_print_ec2_instances(resource):
	response = resource.instances.all()
	for each_item in response.all():
		print(each_item)

#get_and_print_ec2_instances(ec2_console_cli)

def get_and_print_s3_buckets(resource):
	response = resource.buckets.all()
	for each_item in response:
		print(each_item.name)

#get_and_print_s3_buckets(s3_console_cli)