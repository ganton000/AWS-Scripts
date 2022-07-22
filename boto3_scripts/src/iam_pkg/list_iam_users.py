import boto3

def list_iam_users_with_resource(profileName):
	'''
	Resource gives a high-level to AWS resources
	Returns an object but limited in methods

	Note if profileName === 'default', no need to create
	aws_manage_console; since cli automatically sets profile_name='default'
	'''
	aws_manage_console = boto3.session.Session(profile_name=profileName)
	iam_console = aws_manage_console.resource('iam')
	##additional args
	#iam_console = aws_manage_console.resource(service_name='iam', region_name='us-east-1')

	return [ print(each_user) for each_user in iam_console.users.all()]

def list_iam_users_with_client(profileName):
	'''
	Client gives low-level to AWS resources
	Returns a dictionary and requires more logic
	'''
	aws_manage_console = boto3.session.Session(profile_name=profileName)
	iam_console = aws_manage_console.client('iam')

	return [ print(each_user['UserName']) for each_user in iam_console.list_users()['Users'] ]


#list_iam_users_with_resource('default')
#list_iam_users_with_client('default')