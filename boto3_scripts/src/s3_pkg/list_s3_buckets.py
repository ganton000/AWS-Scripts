import boto3

profileName = "default"
aws_manage_console = boto3.session.Session(profile_name=profileName)

def list_s3_buckets():
	s3_console = aws_manage_console.resource('s3')

	return [ print(each_bucket) for each_bucket in s3_console.buckets.all() ]

#list_s3_buckets()

bucket_name = 'contents.anton.ai'

def print_s3_objects_with_resource(bucket_name):
	s3_res = aws_manage_console.resource('s3')
	bucket_object = s3_res.Bucket(bucket_name)
	count = 1
	for each_obj in bucket_object.objects.all():
		print(count, each_obj.key)
		count +=1

#print_s3_objects_with_resource(bucket_name)

def print_s3_objects_with_client(bucket_name):
	s3_client = aws_manage_console.client('s3')

	count = 1
	for each_obj in s3_client.list_objects(Bucket=bucket_name)['Contents']:
		print(count, each_obj.get('Key'))
		count +=1

#print_s3_objects_with_client(bucket_name)


def paginate_and_print_s3_objects_with_client(bucket_name):
	s3_client = aws_manage_console.client('s3')
	paginator = s3_client.get_paginator('list_objects')

	count = 1
	for each_page in paginator.paginate(Bucket=bucket_name):
		for each_obj in each_page['Contents']:
			print(count, each_obj['Key'])
			count += 1

paginate_and_print_s3_objects_with_client(bucket_name)