import sys

try:
	import boto3
	import botocore
except ModuleNotFoundError:
	print("Boto3 is not installed. pip3 install boto3")
	sys.exit(1)
except Exception as e:
	print(e)
	sys.exit(2)

print(dir(boto3.exceptions))
print("=============================")
print()

#Boto3 is built on top of botocore.
##can access more exceptions using botocore
print(dir(boto3.exceptions.botocore.exceptions))
print("=============================")
print()

try:
	aws_mng_con=boto3.session.Session(profile_name="dev")
except botocore.exceptions.ProfileNotFound as e:
	print("Dev profile is not configured on .aws credentials. Will attempt to use default profile instead")
	aws_mng_con=boto3.session.Session(profile_name="default")
except Exception as e:
	print(e)
	sys.exit(3)

try:
	iam_con_res = aws_mng_con.resource(service_name='iam', region_name='us-east-1')
except botocore.exceptions.ClientError as e:
	#print(dir(e))
	if e.response['Error']['Code'] == "AccessDenied":
		print(e.response['Error']['Message'])
	else:
		print(e.response['Error']['Code'])
		print(e.response['Error']['Message'])
	sys.exit(4)
except Exception as e:
	print(e)
	sys.exit(5)



