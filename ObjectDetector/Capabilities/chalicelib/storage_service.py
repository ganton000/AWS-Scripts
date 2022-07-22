import boto3

class StorageService:
	def __init__(self, storage_location: str):
		self.client = boto3.client('s3')
		self.bucket_name = storage_location

	def get_storage_location(self) -> str:
		return self.bucket_name

	def list_files(self) -> list[dict]:
		#Returns up to 1000 of the objects in bucket per request.
		response = self.client.list_objects_v2(Bucket=self.bucket_name)

		files = []
		for content in response['Contents']:
			files.append({
				'location': self.bucket_name,
				'file_name': content['Key'],
				'url': "http://" + self.bucket_name + ".s3.amazonaws.com/" + content['Key']
			})
		return files