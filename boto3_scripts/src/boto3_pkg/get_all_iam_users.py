import boto3

profileName = "default"

session = boto3.session.Session(profile_name=profileName)
iam_res = session.resource("iam")


def get_and_print_iam_users_with_res():
	count = 1
	for each_user in iam_res.users.all():
		print(count, each_user.user_name)
		count += 1

#get_and_print_iam_users_with_res()

iam_client = session.client("iam")

def get_and_print_iam_users_with_client():
	count = 1
	for each_user in iam_client.list_users()['Users']:
		print(count, each_user['UserName'])
		count += 1

#get_and_print_iam_users_with_client()

def paginate_and_print_users():
	paginator = iam_client.get_paginator('list_users')
	count = 1
	for each_page in paginator.paginate():
		for each_user in each_page['Users']:
			print(count, each_user['UserName'])
			count += 1

#paginate_and_print_users()

def paginate_and_print_s3_objects(bucket_id):
	paginator = iam_client.get_paginator('list_objects')
	count = 1
	for each_page in paginator.paginate(Bucket=bucket_id):
		print(each_page)