import boto3


def get_user_details(profileName, username):
	session = boto3.session.Session(profile_name=profileName)
	iam_con_res = session.resource(service_name="iam")

	iam_user_obj = iam_con_res.User(username)
	print(f'Username: {iam_user_obj.user_name}')
	print(f'UserID: {iam_user_obj.user_id}')
	print(f'ARN: {iam_user_obj.arn}')
	print(f'Date Created: {iam_user_obj.create_date.strftime("%m-%d-%Y")}')
	print()

def get_details_of_users(profileName):
	session = boto3.session.Session(profile_name=profileName)
	iam_con_res = session.resource(service_name="iam")

	for iam_user_obj in iam_con_res.users.all():
		print(f'Username: {iam_user_obj.user_name}')
		print(f'UserID: {iam_user_obj.user_id}')
		print(f'ARN: {iam_user_obj.arn}')
		print(f'Date Created: {iam_user_obj.create_date.strftime("%m-%d-%Y")}')
		print()


if __name__ == "__main__":

	profileName = "default"
	username = "Harry"


	#get_user_details(profileName, username)
	get_details_of_users(profileName)