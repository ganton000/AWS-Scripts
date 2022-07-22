import boto3

session = boto3.session.Session(profile_name="aws-lex-ai")

class StorageService:
	def __init__(self):
		self.s3 = session.resource('s3')

	def get_all_files(self, storage_location):
		'''
		Returns list of s3 objects
		'''
		return self.s3.Bucket(storage_location).objects.all()
