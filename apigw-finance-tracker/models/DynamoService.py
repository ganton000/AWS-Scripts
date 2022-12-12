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

class DynamoService:


	def __init__(self, ddb_client: object) -> None:
		self.ddb_client = ddb_client

