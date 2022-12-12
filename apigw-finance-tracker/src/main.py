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

#api_url = f"https://{api_id}.execute-api.{region}.amazonaws.com/{stage}"

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
		"path": "transactions/{id}",
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


""" --- MAIN HANDLER --- """
def main():
	pass

if __name__ == "__main__":

	main()