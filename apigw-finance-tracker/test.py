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
apigw = boto3.client("apigateway")


def list_apis():
	apis = apigw.get_rest_apis()["items"]
	return apis

def get_api_resources(rest_api_id: str):
	resources = apigw.get_resources(
		restApiId=rest_api_id
	)["items"]
	logger.info(resources)

def main():
	api_id = list_apis()[0]["id"]
	get_api_resources(api_id)

if __name__ == "__main__":
	main()