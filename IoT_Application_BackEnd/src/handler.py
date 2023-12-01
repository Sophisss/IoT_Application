import json
import os
from services.generation.generator_service import generate_code
from services.response import http_status_code
from services.storage.storage_service import StorageService


def download_code(event, context):
    """
    Lambda function to generate a code, put it into an S3 bucket, and return the URL of the generated code.
    :param event: input event that triggers the Lambda function.
    :param context: context information about the execution environment.
    :return: a response containing the URL of the generated code.
    """
    storage_service = StorageService(os.environ['BUCKET_NAME'])
    code_generated = generate_code(json.loads(event['body']))
    try:
        storage_service.create_zip_and_upload_code(code_generated)
        url = storage_service.create_url()

        return http_status_code.ok(json_body=json.dumps({
            "message": "Object uploaded successfully",
            "url": url}))

    except Exception as e:
        return http_status_code.internal_server_error(json_body=json.dumps({"error": str(e)}))
