import json
import os
import zipfile
import utility_methods as utilities
from io import BytesIO
from generate_code_api import generate_template_api
from generazione_lambda import generate_lambda_code


def download_zip_code(event, context):
    """
    This function download the code from S3 bucket.
    :param event: The event.
    :param context: The context.
    :return: Response.
    """
    bucket_name = os.environ['BUCKET_NAME']
    folder_name = os.environ['FOLDER_NAME']
    file_name = 'api.py'  # TODO: rivedi

    utilities.check_response(create_folder(bucket_name, folder_name))
    utilities.check_response(put_file(bucket_name, folder_name, file_name))
    generate_code(bucket_name, folder_name)
    create_zip(bucket_name, folder_name, zip_key='code.zip')
    return {"body": json.dumps({"url": create_url(bucket_name, zip_key='code.zip')})}


def create_folder(bucket_name, folder_name):
    """
    This function create a folder in S3 bucket.
    :param bucket_name: S3 bucket name.
    :param folder_name: S3 folder name.
    :return: Response.
    """
    response = utilities.put_s3_object(bucket_name, f'{folder_name}/')
    return utilities.handle_response(response, 'Folder created successfully')


def put_file(bucket_name, folder_name, file_name):  # TODO: chiedere a massi perché non serviva
    """
    This function upload a file to S3 bucket.
    :param bucket_name: S3 bucket name.
    :param folder_name: S3 folder name.
    :param file_name: the file name.
    :return: Response.
    """
    key = os.path.join(folder_name, file_name)
    with BytesIO(b'') as empty_file:
        response = utilities.put_s3_object(bucket_name, key, archive=empty_file.read())
    return utilities.handle_response(response, 'File uploaded successfully')


def generate_code(bucket_name, folder_name):
    """
    This function generate the code.
    :param bucket_name: S3 bucket name.
    :param folder_name: S3 folder name.
    :return: Response.
    """
    generate_lambda_code(bucket_name, folder_name)
    # generate_template_api(bucket_name, folder_name)
    # generate_template_cognito(bucket_name, folder_name)


def create_zip(bucket_name, folder_name, zip_key=None):
    """
    This function create a zip file from a list of objects.
    :param bucket_name: S3 bucket name.
    :param folder_name: S3 folder name.
    :param zip_key: S3 object key.
    """
    with BytesIO() as archive:
        with zipfile.ZipFile(archive, 'w') as zip_file:
            for obj in list_objects(bucket_name, folder_name):
                file_body = utilities.get_s3_object(bucket_name, obj['Key'])['Body'].read()
                zip_file.writestr(obj['Key'], file_body)

        archive.seek(0)
        utilities.get_s3_client().upload_fileobj(archive, bucket_name, zip_key)


def list_objects(bucket_name, folder_name):
    """
    This function list all the objects in a folder.
    :param bucket_name: S3 bucket name.
    :param folder_name: S3 folder name.
    :return: List of objects.
    """
    objects = utilities.get_s3_client().list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
    return objects.get('Contents', [])


def create_url(bucket_name, zip_key=None):
    """
    This function create a presigned URL for an S3 object.
    :param bucket_name: S3 bucket name.
    :param zip_key: S3 object key.
    :return: Presigned URL.
    """
    return utilities.get_s3_client().generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name,
                'Key': zip_key},
        ExpiresIn=3600)
