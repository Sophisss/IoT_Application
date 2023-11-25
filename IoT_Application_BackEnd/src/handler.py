import json
from services.generation.generator_service import generate_code
from services.storage.storage_service import Storage


def download_zip_code(event, context):
    """
    Lambda function to generate a code, put it into an S3 bucket, create a zip file,
    and return a URL pointing to the zip file.
    :param event: input event that triggers the Lambda function.
    :param context: context information about the execution environment.
    :return: a response containing the URL of the generated zip file.
    """
    storage_instance = Storage()
    json_data = json.loads(event['body'])
    code_generated = generate_code(json_data)
    response = storage_instance.put_object_to_s3(code_generated)

    if response['statusCode'] == 200:
        storage_instance.create_zip(code_generated.keys())
        return storage_instance.create_url()

    return response
