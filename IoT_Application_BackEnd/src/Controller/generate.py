import json
import os
import boto3
import requests


def create_presigned_url(event, context):
    s3_client = boto3.client('s3')
    bucket_name = os.environ['BUCKET_NAME']
    folder_name = os.environ['FOLDER_NAME']

    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name,
                    'Key': folder_name},
            ExpiresIn=3600)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'url': response
            })
        }
    except Exception as error:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error while getting presigned url',
                'error': str(error)
            })
        }


def create_presigned_post(bucket_name, folder_name):
    s3_client = boto3.client('s3')

    response = s3_client.generate_presigned_url(
        'put_object',
        Params={'Bucket': bucket_name,
                'Key': folder_name},
        ExpiresIn=3600)
    return response


def putFileToS3(event, context):
    try:
        presigned_url = create_presigned_post(os.environ['BUCKET_NAME'], os.environ['FOLDER_NAME'])

        with open('../../templates/prova.yaml', 'rb') as file:
            response = requests.put(presigned_url, data=file)

        if response.status_code == 200:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'File uploaded successfully'
                })
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'message': 'Error while uploading file',
                    'response': response.text
                })
            }
    except Exception as error:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error during file upload',
                'error': str(error)
            })
        }