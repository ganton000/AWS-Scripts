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

#initialize client
apigw = boto3.client("apigateway")
lambda_client = boto3.client("lambda")
sts = boto3.client('sts')

#Define routes
routes = [
	{
		"path": "/transactions",
		"method": "POST",
		"functionName": "add_transaction"
	},
	{
		"path": "/transactions",
		"method": "GET",
		"functionName": "get_transactions"
	},
	{
		"path": "/transactions/{id}",
		"method": "GET",
		"functionName": "get_transaction"
	},
	{
		"path": "/transactions/{id}",
		"method": "DELETE",
		"functionName": "delete_transaction"
	}
]

""" --- HELPER FUNCTIONS --- """

""" --- API CALLS --- """
def add_permission_to_lambda(lambda_name: str, principal_arn: str, api_base_path: str) -> None:
	"""Adds trust permission policy to a specified lambda so API Gateway can invoke it"""

	source_arn = f"{principal_arn}/*/*/{api_base_path}"
	try:
		lambda_client.add_permission(
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


""" --- MAIN HANDLER --- """
def main():
	pass

if __name__ == "__main__":

	#initialize variables
	account_id = sts.get_caller_identity()['Account']
	api_name = "finance-tracker"
	api_base_path = "transactions"
	api_stage = "dev"