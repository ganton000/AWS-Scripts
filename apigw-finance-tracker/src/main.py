import json
import logging
from typing import List, Optional

import boto3

#initialize logger
logging.basicConfig(
	format="%(asctime)s %(message)s",
	datefmt="%m/%d/%Y %I:%M:%S %p",
	level=logging.INFO
	)
logger = logging.getLogger(__name__)

#initialize client
apigw = boto3.client("apigateway")

class ApiGatewayService:

	def __init__(self, apigw_client):
		self.apigw_client = apigw_client
		self.api_id = None
		self.root_id = None
		self.stage = None

	def create_rest_api(self, api_name: str, api_desc: Optional[str]=None) -> None:
		#The default API has only a root resource and no HTTP methods

		try:
			response = self.apigw_client.create_rest_api(
				name=api_name,
				description= api_desc if api_desc is not None else api_name
			)

			self.api_id = response["id"]
			logger.info(f"Created REST API {api_name} with id {self.api_id}")

		except Exception as err:
			logger.exception(f"Couldn't create REST API {api_name}")
			raise err

	def add_rest_resource(self, parent_id: str, resource_path: str) -> str:
		"""Adds a resource to a REST API.

		Args:
			parent_id (str): The ID of the parent resource
			resource_path (str): Path of the new resource, relative to the parent.

		Raises: err

		Return: The ID of the new resource
		"""

		try:
			response = self.apigw_client.create_resource(
			restApiId=self.api_id,
			parentId=parent_id,
			pathPart=resource_path
			)

			resource_id = response["id"]
			logger.info(f"Created resource {resource_path} with ID {resource_id}")

		except Exception as err:
			logger.exception(f"Couldn't create resource {resource_path}")
			raise err
		else:
			return resource_id

	def deploy_api(self, stage_name: str):
		""" After a REST API is deployed, it can be called from any
        REST client, such as the Python Requests package or Postman.

		Args:
			stage_name (_type_): stage of the API to deploy; i.e. 'tst'.

		Returns: base URL of the deployed REST API.
		"""

		self.stage = stage_name
		try:
			self.apig_client.create_deployment(
                restApiId=self.api_id,
				stageName=stage_name
			)

			logger.info(f"Deployed to stage {stage_name}")
		except Exception as err:
			logger.exception(f"Couldn't deploy to stage {stage_name}")
			raise err
		else:
			return self.api_url

	def api_url(self, resource: Optional[str]=None) -> str:
		""" Builds the REST API URL from its parts.

		Args:
			resource (str): The resource path to append to the base URL.

		Returns: The REST URL to the specified resource
		"""

		url = f"https://{self.api_id}.execute-api.{self.apigw_client.meta.region_name}.amazonaws.com/{self.stage}"

		url = f"{url}/{resource}" if resource is not None else url

		return url






