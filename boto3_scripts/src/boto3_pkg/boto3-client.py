import boto3

aws_manage_console = boto3.session.Session(profile_name='default');

#initialize iam, ec2, s3 console
iam_console_cli = aws_manage_console.client(service_name='iam', region_name='us-east-1')
ec2_console_cli = aws_manage_console.client(service_name='ec2', region_name='us-east-1')
s3_console_cli = aws_manage_console.client(service_name='s3', region_name='us-east-1')

#List all iam users using client object
def get_and_print_iam_users(client):
	user_list = client.list_users()['Users']
	for user in user_list:
		print(user['UserName'])

#get_and_print_iam_users(iam_console_cli)

def get_and_print_ec2_instance_ids(client):
	item_list = client.describe_instances()['Reservations']
	for each_item in item_list:
		print(each_item['Instances'])


#get_and_print_ec2_instance_ids(ec2_console_cli)

def get_and_print_s3_buckets(client):
	bucket_list = client.list_buckets()['Buckets']
	for bucket in bucket_list:
		print(bucket['Name'])

#get_and_print_s3_buckets(s3_console_cli)