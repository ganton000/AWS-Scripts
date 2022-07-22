import boto3

def get_account_id(profileName):
	aws_mag_con = boto3.session.Session(profile_name=profileName)
	sts_console_cli = aws_mag_con.client(service_name='sts', region_name='us-east-1')
	response = sts_console_cli.get_caller_identity()
	print(f"User ID: {response['UserId']}")
	print(f"Account ID: {response['Account']}")
	return response.get('Account')

def get_all_snapshots(profileName):
	'''
	can use client.describe_snapshots(OwnerIds=my_id) as alternative
	'''
	aws_mag_con = boto3.session.Session(profile_name=profileName)
	ec2_con_res = aws_mag_con.resource(service_name='ec2', region_name='us-east-1')

	my_id = [get_account_id(profileName)]
	res = []
	for snapshot in ec2_con_res.snapshots.filter(OwnerIds=my_id):
		print(snapshot)
		res.append(snapshot)

	return res

if __name__ == "__main__":

	profileName = "default"

	get_all_snapshots(profileName)