import json
import os
import boto3

s3 = boto3.client('s3')


def lambda_handler(event, context):
    bucket_name = os.environ['BUCKET_NAME']
    folder_name = os.environ['FOLDER_NAME']

    url = f'https://{bucket_name}.s3.amazonaws.com/{folder_name}/'

    return {
        'statusCode': 200,
        'body': json.dumps({'url': url})
    }
