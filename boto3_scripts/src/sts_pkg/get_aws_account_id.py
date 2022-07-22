import boto3


#A low-level client representing AWS Security Token Service (STS)
#Security Token Service (STS) enables you to request temporary, limited-privilege credentials for Identity and Access Management (IAM) users or for users that you authenticate (federated users).

def get_user_and_account_id(profileName):
	aws_manage_console = boto3.session.Session(profile_name=profileName)
	sts_console_cli = aws_manage_console.client(service_name='sts', region_name='us-east-1')
	response = sts_console_cli.get_caller_identity()
	print(f"User ID: {response['UserId']}")
	print(f"Account ID: {response['Account']}")

get_user_and_account_id('default')

