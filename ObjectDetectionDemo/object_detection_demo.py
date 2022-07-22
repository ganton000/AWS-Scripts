from storage_service import StorageService
from recognition_service import RecognitionService
import sys

storage_service = StorageService()
recognition_service = RecognitionService()

bucket_name = sys.argv[1]
for file in storage_service.get_all_files(bucket_name):
	'''
	Gets all JPG images in specified S3 bucket
	Performs object detection on each image using AWS Rekognition
	Prints out labels along with confidence scores for objects detected
	in .jpg file
	'''
	if file.key.endswith('.jpg'):
		print('Objects detected in image ' + file.key + ':')
		labels = recognition_service.detect_objects(file.bucket_name, file.key)

		for label in labels:
			print( '--' + label['Name'] + ': ' + str(label['Confidence']))