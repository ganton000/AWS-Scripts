import json
import os
import boto3
import uuid
from io import BytesIO
from PIL import Image, ImageOps

region = str(os.getenv('REGION_NAME'))
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
ddb = boto3.resource('dynamodb', region_name=region)

dbtable = str(os.getenv('DYNAMODB_TABLE'))

def detect_faces(bucket, key):
    response = rekognition.detect_faces(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": key
            }
        },
        Attributes= ['ALL']
    )
    return response

def detect_labels(bucket, key):
    response = rekognition.detect_labels(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": key
            }
        }
    )
    return response

def index_faces(bucket, key):
    rekognition.create_collection(CollectionId='BLUEPRINT_COLLECTION')
    response = rekognition.index_faces(
        Images={
            "S3Object": {
                "Bucket": bucket,
                "Name": key
            }
        },
        CollectionId="BLUEPRINT_COLLECTION"
    )

    return response

def list_faces(event, context):

    table = ddb.Table(dbtable)
    response = table.scan()
    data = response['Items']

    #paginate through results
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey= response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(data)
    }

def get_s3_image_url(bucket, key):
    #image object url
    url = '{}/{}/{}'.format(s3.meta.endpoint_url, bucket, key)

    return url

def lambda_handler(event, context):
    '''
    Demonstrates S3 trigger that uses
    Rekognition APIs to detect faces, labels and index faces in S3 Object.
    '''

    #Get object from event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    #get uploaded image url
    image_url = get_s3_image_url(bucket, key)
    print("--->> URL: "+ image_url)

    try:
        # Calls rekognition DetectFaces API to detect faces in S3 object
        response = detect_faces(bucket, key)

        # Calls rekognition DetectLabels API to detect labels in S3 object
        #response = detect_labels(bucket, key)

        # Calls rekognition IndexFaces API to detect faces in S3 object and index faces into specified collection
        #response = index_faces(bucket, key)

        # Print response to console.
        print(response)
        data = []

        for faceDetail in response['FaceDetails']:

            item = {
                'id': str(uuid.uuid4()),
                "dataType": "Emotions",
                "image_url": image_url}

            item[str(faceDetail['Gender']['Value']).lower()] = str(
                faceDetail['Gender']['Confidence'])
            item["eyesopen"] = {
                str(faceDetail['EyesOpen']['Value']): str(
                    faceDetail['EyesOpen']['Confidence'])

            }
            # print('Emotions: \t Confidence\n')
            for emotion in faceDetail['Emotions']:
                item[str(emotion['Type']).lower()] = str(emotion['Confidence'])

                # print(str(emotion['Type']) + '\t\t' +
                #       str(emotion['Confidence']))
            data.append(item)

        emotion_payload = json.dumps(data)

        # SAVE PAYLOAD TO DYNAMODB
        table = dynamodb.Table(dbtable)
        print(item)
        response = table.put_item(
            Item=item
        )
      # save_response_to_db(payload=emotion_payload)

        print('::::==> ' + emotion_payload)
        return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e