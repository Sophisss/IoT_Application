from io import BytesIO
import boto3
import zipfile
import os


def get_bucket_name():
    return os.environ['BUCKET_NAME']


def get_s3_client():
    """
    This function initialize the S3 client.
    :return: S3 client.
    """
    return boto3.client('s3')


def put_object_to_s3(codes: list[str]):
    key = 'code_generated/api.py'
    for code in codes:
        get_s3_client().put_object(Bucket=get_bucket_name(), Key=key, Body=code)


def create_zip():
    bucket_name = get_bucket_name()
    with BytesIO() as archive:
        with zipfile.ZipFile(archive, 'w') as zip_file:
            for obj in list_objects(bucket_name, 'code_generated'):
                file_body = get_s3_object(bucket_name, obj['Key'])['Body'].read()
                zip_file.writestr(obj['Key'], file_body)

        archive.seek(0)
        get_s3_client().upload_fileobj(archive, bucket_name, 'code.zip')


def get_s3_object(bucket_name, key):
    """
    This function retrieve the content of an S3 object.
    :param bucket_name: S3 bucket name.
    :param key: S3 object key.
    :return: S3 object content.
    """
    return get_s3_client().get_object(Bucket=bucket_name, Key=key)


def list_objects(bucket_name, folder_name):
    """
    This function list all the objects in a folder.
    :param bucket_name: S3 bucket name.
    :param folder_name: S3 folder name.
    :return: List of objects.
    """
    objects = get_s3_client().list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
    return objects.get('Contents', [])


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
