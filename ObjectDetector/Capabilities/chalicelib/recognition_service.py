import boto3
from typing import Type
from .storage_service import StorageService

class RecognitionService:
	def __init__(self, storage_service: Type[StorageService]) -> None:
		self.client = boto3.client('rekognition')
		self.bucket_name = storage_service.get_storage_location()

	def detect_objects(self, file_name: str) -> list[dict]:
		response = self.client.detect_labels(
			Image = {
				"S3Object": {
					"Bucket": self.bucket_name,
					"Name": file_name
				}
			}
		)

		objects = []
		for label in response["Labels"]:
			objects.append({
				"label": label['Name'],
				"confidence": label['Confidence']
			})

		return objects
