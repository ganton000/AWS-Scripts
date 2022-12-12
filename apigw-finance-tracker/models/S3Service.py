import logging
from typing import List, Optional

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

