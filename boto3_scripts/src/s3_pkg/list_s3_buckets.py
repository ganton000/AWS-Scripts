import boto3

profileName = "default"

def list_s3_buckets(profileName):
	aws_manage_console = boto3.session.Session(profile_name=profileName)
	s3_console = aws_manage_console.resource('s3')

	return [ print(each_bucket) for each_bucket in s3_console.buckets.all() ]

list_s3_buckets(profileName)