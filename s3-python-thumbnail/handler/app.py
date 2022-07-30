from datetime import datetime
import boto3
from io import BytesIO
#Added layer for PIL import (pillow)
from PIL import Image, ImageOps
import os
import uuid
import json

s3 = boto3.client("s3")
size = int(os.getenv("THUMBNAIL_SIZE"))
dbtable = str(os.getenv("DYNAMODB_TABLE"))
region = str(os.getenv("REGION_NAME"))

ddb = boto3.resource('dynamodb', region_name=region)

def s3_thumbnail_generator(event, context):
    print("Event::", event)

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    img_size = event['Records'][0]['s3']['object']['size']

    if (not key.endswith("_thumbnail.png")):
        image = get_s3_image(bucket, key)

        thumbnail = image_to_thumbnail(image)

        thumbnail_key = new_filename(key)

        url = upload_to_s3(bucket, thumbnail_key, thumbnail, img_size)

        return url


def get_s3_image(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    imageContent = response['Body'].read()

    file = BytesIO(imageContent)
    img = Image.open(file)
    return img

def image_to_thumbnail(image):
    return ImageOps.fit(image, (size, size), Image.ANTIALIAS)

def new_filename(key):
    key_split = key.rsplit('.', 1)
    return key_split[0] + "_thumbnail.png"

def upload_to_s3(bucket, key, image, img_size):
    #Save image into a BytesIO object to avoid writing to disk
    out_thumbnail = BytesIO()

    image.save(out_thumbnail, 'PNG')
    out_thumbnail.seek(0)

    response = s3.put_object(
        ACL='public-read',
        Body=out_thumbnail,
        Bucket=bucket,
        ContentType='image/png',
        Key=key
    )

    print("Response:: ", response)

    url = '{}/{}/{}'.format(s3.meta.endpoint_url, bucket, key)

    #save image url to db
    s3_save_thumbnail_url_to_dynamo(url_path=url, img_size=img_size)

    return url

def s3_save_thumbnail_url_to_dynamo(url_path, img_size):
    toint = float(img_size*0.53)/1000
    table = ddb.Table(dbtable)
    response = table.put_item(
        Item={
            'id': str(uuid.uuid4()),
            'url': str(url_path),
            'approxReducedSize': str(toint) + str(' KB'),
            'createdAt': str(datetime.now()),
            'updatedAt': str(datetime.now())
        }
    )

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(response)
    }

def s3_get_thumbnail_urls(event, context):
    '''
    get all image urls from ddb and show in json format
    '''
    table = ddb.Table(dbtable)
    response = table.scan()
    data = response['Items']

    #paginate through results
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(data)
    }

def s3_get_item(event, context):
    table = ddb.Table(dbtable)
    response = table.get_item(Key={
        'id': event['pathParameters']['id']
    })

    item = response['Item']

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(item),
        'isBase64Encoded': False
    }