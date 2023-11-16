import json
import boto3
import http_status_code
from io import BytesIO


def get_s3_client():
    """
    This function initialize the S3 client.
    :return: S3 client.
    """
    return boto3.client('s3')


def read_json():
    """
    This function read the JSON file and returns its content.
    :return: JSON file content.
    """
    with open('../../old_code/structure.json', 'r') as opened_file:
        return json.loads(opened_file.read())


def generate_resource_name(resource):
    """
    This function generate the resource name.
    :param resource: The resource.
    :return: The resource name.
    """
    return resource.get("name") or f"{resource['first_entity']}{resource['second_entity']}"


def handle_response(response, success_message):
    """
    This function handles the API response and creates a standardized response.
    :param response: API response.
    :param success_message: Success message.
    :return: Standardized response.
    """
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    error_message = response.get('Error', {}).get('Message')

    if 200 <= status_code < 300:
        return http_status_code.ok(json_body=success_message)
    elif status_code == 403:
        return http_status_code.forbidden(json_body=error_message)
    elif status_code == 404:
        return http_status_code.not_found(json_body=error_message)
    elif 500 <= status_code < 500:
        return http_status_code.internal_server_error(json_body=error_message)
    else:
        return http_status_code.bad_request(json_body=error_message)


def check_response(response):
    """
    Check if the response is successful; if not, return the response.
    :param response: API response.
    :return: Response.
    """
    return response if response['statusCode'] != 200 else None


def get_s3_object(bucket_name, key):
    """
    This function retrieve the content of an S3 object.
    :param bucket_name: S3 bucket name.
    :param key: S3 object key.
    :return: S3 object content.
    """
    return get_s3_client().get_object(Bucket=bucket_name, Key=key)


def put_s3_object(bucket_name, key, archive=None):
    """
    This function put an object in S3 bucket.
    :param bucket_name: S3 bucket name.
    :param key: S3 object key.
    :param archive: Archive.
    :return: S3 object content.
    """
    return get_s3_client().put_object(Bucket=bucket_name, Key=key) if archive is None else get_s3_client().put_object(
        Bucket=bucket_name, Key=key, Body=archive)


def create_archive(yaml, template):
    """
    This function create an archive.
    :param yaml: YAML object.
    :param template: CloudFormation template.
    :return: Archive.
    """
    archive = BytesIO()
    yaml.dump(template, archive)
    archive.seek(0)
    return archive
