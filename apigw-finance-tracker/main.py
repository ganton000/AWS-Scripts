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
def create_rest_api(api_name: str, api_desc: str) -> str:
	try:
		response = apigw.create_rest_api(
			name=api_name,
			description=api_desc
		)

		logger.info(f"Rest API for {api_name} has been successfully created!")

		return response["id"]

	except Exception as err:
		logger.exception(err)
		exit(1)

def create_api_route(api_id: str, route_params: List[dict], lambda_uri: Optional[str]=None):

	method_response = {
		"string" : {
					"statusCode": "200",
					"responseParameters": {
						"method.response.header.Access-Control-Allow-Origin": False
					}
				}
	}

	integration_responses = {
		"string": {
			"statusCode": "200",
			"responseParameters": {
				"method.response.header.Access-Control-Allow-Origin": "'*'"
			}
		}
	}

	method_integration =  {
		"type": "AWS_PROXY",
		"httpMethod": route_params["method"],
		"uri": "",
		"integrationResponses": integration_responses
	}



	resource_methods = {
		route_params["path"]: {
			"httpMethod": route_params["method"],
			"authorizationType": "NONE",
			"methodResponses": method_response,
			"methodIntegration": method_integration
		}
	}

	try:
		apigw.create_resource(
			restApiId=api_id,
			parentId=,
			pathPart=
		)

	except Exception as err:
		print(err)
		exit(1)

""" --- MAIN HANDLER --- """
def main():
	pass

if __name__ == "__main__":

	main()