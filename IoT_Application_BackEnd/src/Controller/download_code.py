import json
import os
import zipfile
from io import BytesIO
import boto3
import generate_code

# Initialize the S3 client and resource
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')


# Function to handle API response and create a standardized response.
def handle_response(response, success_message):
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {'statusCode': 200, 'body': success_message}
    else:
        return {'statusCode': 500, 'body': json.dumps({'message': response['Error']['Message']})}


# Function to create a folder in S3 bucket.
def create_folder(bucket_name, folder_name):
    response = s3_client.put_object(Bucket=bucket_name, Key=f'{folder_name}/')
    return handle_response(response, 'Folder created successfully')


# Function to upload a file to S3 bucket.
def put_file_to_s3(bucket_name, folder_name, file_name):
    key = os.path.join(folder_name, file_name)
    with BytesIO(b'') as empty_file:
        response = s3_client.put_object(Bucket=bucket_name, Key=key, Body=empty_file.read())
    return handle_response(response, 'File uploaded successfully')


# Function to create a presigned URL for an S3 object.
def create_url(bucket_name, zip_key):
    response = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name,
                'Key': zip_key},
        ExpiresIn=3600)
    return response


# Function to generate a zip file from a folder in S3 bucket.
def generate_zip_url(bucket_name, folder_name):
    zip_key = 'code.zip'

    try:
        objects = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)

        with BytesIO() as archive:
            with zipfile.ZipFile(archive, 'w') as zip_file:
                for obj in objects.get('Contents', []):
                    file_key = obj['Key']
                    file_body = s3_resource.Object(bucket_name, file_key).get()['Body'].read()
                    zip_file.writestr(file_key, file_body)

            archive.seek(0)
            s3_client.upload_fileobj(archive, bucket_name, zip_key)

        zip_url = create_url(bucket_name, zip_key)

        if zip_url:
            return {'statusCode': 200, 'body': zip_url}

    except Exception as error:
        return {'statusCode': 500,
                'body': json.dumps({'message': 'Error during zip file generation', 'error': str(error)})}


# Lambda function to orchestrate the process.
def download_zip_code(event, context):
    bucket_name = os.environ['BUCKET_NAME']
    folder_name = os.environ['FOLDER_NAME']
    file_name = 'prova.yaml'

    # Create folder
    response_folder = create_folder(bucket_name, folder_name)
    if response_folder['statusCode'] != 200:
        return response_folder

    # Put file to S3
    response_put = put_file_to_s3(bucket_name, folder_name, file_name)
    if response_put['statusCode'] != 200:
        return response_put

    # Generate templates
    response_generate = generate_code.generate_templates(file_name, bucket_name, folder_name)
    if response_generate['statusCode'] != 200:
        return response_generate

    # Generate and return zip URL
    try:
        response_generate_zip = generate_zip_url(bucket_name, folder_name)
        if response_generate_zip['statusCode'] == 200:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'File downloaded successfully',
                    'url': response_generate_zip['body']
                })
            }
    except Exception as error:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error during zip file generation', 'error': str(error)})
        }
