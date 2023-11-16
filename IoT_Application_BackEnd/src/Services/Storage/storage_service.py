from io import BytesIO
import boto3
import zipfile
import os


def get_bucket_name():
    """
    This function retrieve the bucket name from environment variables.
    :return: Bucket name.
    """
    return os.environ['BUCKET_NAME']


def get_s3_client():
    """
    This function initialize the S3 client.
    :return: S3 client.
    """
    return boto3.client('s3')


def put_object_to_s3(codes: dict):
    """
    This function upload a codes generated to S3 bucket.
    :param codes: the codes generated to upload.
    """
    for key, value in codes.items():
        get_s3_client().put_object(Bucket=get_bucket_name(), Key=key, Body=value)


def create_zip(keys):
    """
    This function create a zip file from a list of objects.
    """
    bucket_name = get_bucket_name()
    with BytesIO() as archive:
        with zipfile.ZipFile(archive, 'w') as zip_file:
            for obj in list_objects(bucket_name, keys):
                file_body = get_s3_object(bucket_name, obj['Key'])['Body'].read()
                zip_file.writestr(obj['Key'], file_body)

        archive.seek(0)
        get_s3_client().upload_fileobj(archive, bucket_name, 'code.zip')


def get_s3_object(bucket_name: str, key) -> dict:
    """
    This function retrieve the content of an S3 object.
    :param bucket_name: S3 bucket name.
    :param key: S3 object key.
    :return: S3 object content.
    """
    return get_s3_client().get_object(Bucket=bucket_name, Key=key)


def list_objects(bucket_name: str, keys) -> list:
    """
    This function list all the objects in a folder.
    :param bucket_name: S3 bucket name.
    :param keys: List of folders.
    :return: List of objects.
    """
    objects = []
    for folder_name in keys:
        response = get_s3_client().list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
        if 'Contents' in response:
            objects.extend(response['Contents'])

    return objects


def create_url(zip_key='code.zip'):
    """
    This function create a presigned URL for an S3 object.
    :param zip_key: S3 object key.
    :return: Presigned URL.
    """
    return get_s3_client().generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': get_bucket_name(),
                'Key': zip_key},
        ExpiresIn=3600)
