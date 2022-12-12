import logging

import boto3

#initialize logger
logging.basicConfig(
	format="%(asctime)s %(message)s",
	datefmt="%m/%d/%Y %I:%M:%S %p",
	level=logging.INFO
	)
logger = logging.getLogger(__name__)

#initialize client
apigw_client = boto3.client("apigateway")
lambda_client = boto3.client("lambda")
s3_client = boto3.client("s3")
dynamo_client = boto3.client("dynamo")
sts_client = boto3.client("sts")

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


""" --- MAIN HANDLER --- """
def main():
	pass

if __name__ == "__main__":

	#initialize variables
	account_id = sts_client.get_caller_identity()['Account']
	api_name = "finance-tracker"
	api_base_path = "transactions"
	api_stage = "dev"