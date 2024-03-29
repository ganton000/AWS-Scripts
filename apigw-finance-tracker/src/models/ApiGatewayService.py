import json
import logging
from typing import List, Optional

from botocore.exceptions import ClientError
import boto3

#initialize logger
logging.basicConfig(
	format="%(asctime)s %(message)s",
	datefmt="%m/%d/%Y %I:%M:%S %p",
	level=logging.INFO
	)
logger = logging.getLogger(__name__)

class ApiGatewayService:

	def __init__(self, apigw_client: object, account_id: str, api_name: str, stage: str) -> None:
		self.apigw_client = apigw_client
		self._account_id = account_id
		self.api_name = api_name
		self.stage = stage
		self.api_id = None
		self.root_id = None

	def create_rest_api(self, api_desc: Optional[str]=None) -> None:
		#The default API has only a root resource and no HTTP methods

		try:
			response = self.apigw_client.create_rest_api(
				name=self.api_name,
				description= api_desc if api_desc is not None else self.api_name
			)

			self.api_id = response["id"]
			logger.info(f"Created REST API {self.api_name} with id {self.api_id}")

		except ClientError:
			logger.exception(f"Couldn't create REST API {self.api_name}")
			raise

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

		except ClientError:
			logger.exception(f"Couldn't create resource {resource_path}")
			raise
		else:
			return resource_id

	def deploy_api(self) -> None:
		""" After a REST API is deployed, it can be called from any
        REST client, such as the Python Requests package or Postman.

		Args:
			stage_name (_type_): stage of the API to deploy; i.e. 'tst'.
		"""

		try:
			self.apig_client.create_deployment(
                restApiId=self.api_id,
				stageName=self.stage
			)

			logger.info(f"Deployed to stage {self.stage}")
		except ClientError:
			logger.exception(f"Couldn't deploy to stage {self.stage}")
			raise

	def api_url(self, resource: Optional[str]=None) -> str:
		""" Builds the REST API URL from its parts.

		Args:
			resource (str): The resource path to append to the base URL.

		Returns: The REST URL to the specified resource
		"""

		url = f"https://{self.api_id}.execute-api.{self.apigw_client.meta.region_name}.amazonaws.com/{self.stage}"

		url = f"{url}/{resource}" if resource is not None else url

		return url

	def add_integration_method(self, resource_id: str, rest_method: str,
		service_endpoint_prefix: str, service_action: str, service_method: str,
		role_arn: str, mapping_template: dict) -> None:
		"""Adds an integration method to a REST API. An integration method is a REST
        resource, such as '/users', and an HTTP verb, such as GET. The integration
        method is backed by an AWS service, such as Amazon DynamoDB.

		Args:
			resource_id (str): The ID of the REST resource
			rest_method (str): The HTTP verb used with the REST resource
			service_endpoint_prefix (str): The service endpoint that is integrated with this method, such as 'dynamodb'.
			service_action (str): The action that is called on the service, such as 'GetItem'
			service_method (str): The HTTP method of the service request, such as POST.
			role_arn (str): Role ARN that grants API Gateway permission to use the specified action with the service.
			mapping_template (_type_):  A mapping template that is used to translate REST elements, such as query parameters, to the request body format required by the service.
		"""

		service_uri = (f"arn:aws:apigateway:{self.apigw_client.meta.region_name}"
					   f":{service_endpoint_prefix}:action/{service_action}")
		try:
			self.apigw_client.put_method(
				restApiId=self.api_id,
				resourceId=resource_id,
				httpMethod=rest_method,
				authorizationType="NONE"
			)
			self.apigw_client.put_method_response(
				restApiId=self.api_id,
				resourceId=resource_id,
				httpMethod=rest_method,
				statusCode="200",
				responseModels={"application/json": ""}
			)

			logger.info(f"Created {rest_method} method for resource {resource_id}")
		except ClientError:
			logger.exception(f"Couldn't create {rest_method} method for resource {resource_id}")
			raise

		try:

			self.apigw_client.put_integration(
				restApiId=self.api_id,
				resourceId=resource_id,
				httpMethod=rest_method,
				type="AWS",
				integrationHttpMethod=service_method,
				credentials=role_arn,
				requestTemplates={"application/json": json.dumps(mapping_template)},
				uri=service_uri,
				passthroughBehavior="WHEN_NO_TEMPLATES"
			)

			self.apigw_client.put_integration_response(
				restApiId=self.api_id,
				resourceId=resource_id,
				httpMethod=rest_method,
				statusCode="200",
				responseTemplates={"application/json": ""}
			)

			logger.info(f"Created integration for resource {resource_id} to service URI {service_uri}")
		except ClientError:
			logger.info(f"Couldn't create integration for resource {resource_id} to service URI {service_uri}")
			raise


	def get_resources(self) -> List[dict]:

		try:
			response = self.apigw_client.get_resources(
				restApiId=self.api_id
			)["items"]

			return response

		except ClientError:
			logger.exception("Couldn't fetch resources for the REST api.")
			raise

	def get_path_id(self, path: str="/") -> str:

		try:
			resources = self.get_resources()

			path_id = next(item["id"] for item in resources if item["path"] == path)

			#Check if path is root
			if path == "/":
				self.root_id = path_id
				logger.info(f"Found root resource of the REST Api with ID of {path_id}")

			return path_id

		except ClientError:
			logger.exception("Couldn't get ID of the root resource for the REST api.")
			raise

	def delete_rest_api(self) -> None:
		"""Deletes a REST Api and all of its resources from API Gateway
		"""

		try:
			self.apigw_client.delete_rest_api(restApiId=self.api_id)

			logger.info(f"Deleted REST Api with id {self.api_id}")

		except ClientError:
			logger.exception(f"Couldn't delete REST Api with id {self.api_id}")
			raise

	def get_api_arn(self) -> str:

		return (
			f"arn:aws:execute-api:{self.apigw_client.meta.region_name}:"
			f"{self._account_id}:{self.api_id}"
		)
