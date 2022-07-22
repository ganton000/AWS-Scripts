import boto3
import sys
from utils.random_password_generator import generate_password

def get_iam_client(profileName="default"):

	try:
		session = boto3.session.Session(profile_name=profileName)
		iam_client = session.client(service_name="iam", region_name="us-east-1")

		return iam_client
	except Exception as e:
		print(e)
		sys.exit(1)

def get_sts_client(profileName="default"):

	try:
		session = boto3.session.Session(profile_name=profileName)
		sts_client = session.client(service_name="sts", region_name="us-east-1")

		return sts_client

	except Exception as e:
		print(e)
		sys.exit(1)

def get_policy(policy_name, isAWSPolicy=False):
	iam_client = get_iam_client()
	sts_client = get_sts_client()

	if not isAWSPolicy:
		policy_arn = f'arn:aws:iam::aws:policy/{policy_name}'
	else:
		try:
			account_id = sts_client.get_caller_identity()['Account']
			policy_arn = f'arn:aws:iam::{account_id}:policy/{policy_name}'
		except Exception as e:
			print(e)
			sys.exit(2)

	try:
		policy_res = iam_client.get_policy(PolicyArn=policy_arn)['Policy']
	except Exception as e:
		print(e)
		sys.exit(3)

	return policy_res

def create_login_profile(username, password, forcePasswordReset=False):
	'''
	Creates password for specified user,
	allowing user to access AWS through management console.
	'''
	iam_client = get_iam_client()

	try:
		iam_client.create_login_profile(
			UserName=username,
			Password=password,
			PasswordResetRequired=forcePasswordReset
		)
	except Exception as e:
		print(e)
		return

	print(f"Login Profile was created!\n{username} now has access to AWS Management Console")
	return

def attach_policy_to_user(username, policyArn):
	iam_client = get_iam_client()

	try:
		iam_client.attach_user_policy(
			UserName=username,
			PolicyArn=policyArn
		)
	except Exception as e:
		print(e)
		sys.exit(2)

	return

def create_iam_user(username):
	iam_client = get_iam_client()

	try:
		iam_client.create_user(UserName=username)
	except Exception as e:
		if e.response["Error"]["Code"] == "EntityAlreadyExists":
			print(f"An IAM User with {username} already exists!")
			sys.exit(2)
		else:
			print("Please verify the following error and retry")
			print(e)
			sys.exit(2)

	print(f"User: {username} has been successfully created!")
	return

def main():
	iam_user_name = "aws-lex-ai"
	policy_name = "AdministratorAccess"

	iam_user_password = generate_password()
	iam_user_policyArn = get_policy(policy_name)['Arn']

	create_iam_user(iam_user_name)

	create_login_profile(iam_user_name, iam_user_password)

	attach_policy_to_user(iam_user_name, iam_user_policyArn)
	print(f"The {policy_name} policy has been attached to user: {iam_user_name}")
	print(f"Password is {iam_user_password}")


if __name__ == "__main__":
	pass
	#main()
