import logging
from typing import Optional

from botocore.exceptions import ClientError

#initialize logger
logging.basicConfig(
	format="%(asctime)s %(message)s",
	datefmt="%m/%d/%Y %I:%M:%S %p",
	level=logging.INFO
	)
logger = logging.getLogger(__name__)

class S3Service:

	def __init__(self, s3_client: object) -> None:
		self.s3_client = s3_client

	def upload_file(self, file_name: str, bucket_name: str, object_name: Optional[str]=None) -> None:
		"""Upload a file to an S3 bucket

		Args:
			file_name (str): file to upload
			bucket_name (str): bucket to upload file to
			object_name (str, optional): S3 object name. If None then uses file_name. Defaults to None.
		"""

		object_name = object_name if object_name is not None else file_name
		try:
			self.s3_client.upload_file(file_name, bucket_name, object_name)
			logger.info(f"Uploaded {file_name} to {bucket_name}")
		except ClientError:
			logger.exception(f"Couldn't upload {file_name} to {bucket_name}")
			raise