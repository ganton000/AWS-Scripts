import logging

from botocore.exceptions import ClientError

#initialize logger
logging.basicConfig(
	format="%(asctime)s %(message)s",
	datefmt="%m/%d/%Y %I:%M:%S %p",
	level=logging.INFO
	)
logger = logging.getLogger(__name__)

class LambdaService:


	def __init__(self, lambda_client: object) -> None:
		self.lambda_client = lambda_client

	def add_permission_to_lambda(self, lambda_name: str, principal_arn: str, api_base_path: str) -> None:
		"""Adds trust permission policy to a specified lambda so API Gateway can invoke it"""

		source_arn = f"{principal_arn}/*/*/{api_base_path}"
		try:
			self.lambda_client.add_permission(
				FunctionName=lambda_name,
				StatementId="apigw-invoke",
				Action="lambda:InvokeFunction",
				Principal="apigateway.amazonaws.com",
				SourceArn=source_arn
			)

			logger.info(f"Granted Lambda {lambda_name} trust permissions for API Gateway")

		except ClientError:
			logger.exception(f"Couldn't add permission to let API Gateway invoke {lambda_name}")
			raise

