import json
import uuid
from datetime import datetime
import os
import boto3

def lambda_handler(event, context):
	#make sure we have a post
	if ('body' not in event or event['httpMethod'] != 'POST'):
		return {
			'statusCode': 400,
			'headers': {},
			'body': json.dumps({'msg': 'Bad Request'})
		}

	table_name = os.environ.get('DYNAMODB_TABLE', 'Posts')
	region = os.environ.get('REGION_NAME', 'us-east-1')

	ddb = boto3.resource(
		'dynamodb',
		region_name= region
	)

	table = ddb.Table(table_name)

	post_str = event['body']
	post = json.loads(post_str) #convert json to python dict

	current_timestamp = datetime.now().isoformat()

	params = {
		'id': str(uuid.uuid4()),
		'content': post['content'],
		'author': post['author'],
		'createdAt': str(current_timestamp)
	}

	response = table.put_item(
		TableName= table_name,
		Item= params
	)

	print(f'response:: {response}')

	return {
			'statusCode': 200,
			'headers': {},
			'body': json.dumps({'message': 'Post Created!'})
		}
