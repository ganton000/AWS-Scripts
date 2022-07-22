import boto3

profileName = 'default'

aws_mag_con = boto3.session.Session(profile_name=profileName)
ec2_con_res = aws_mag_con.resource(service_name='ec2', region_name='us-east-1')

def get_account_id(profileName):
	sts_console_cli = aws_mag_con.client(service_name='sts', region_name='us-east-1')
	response = sts_console_cli.get_caller_identity()
	print(f"User ID: {response['UserId']}")
	print(f"Account ID: {response['Account']}")
	return response.get('Account')



def get_snaps_by_size(profileName):
	my_id = [get_account_id(profileName)]
	f_size = {
		"Name": "volume-size",
		"Values": ["8", "10"]
	}
	for snapshot in ec2_con_res.snapshots.filter(OwnerIds=my_id, Filters=[f_size]):
		print(snapshot)

get_snaps_by_size(profileName)