import json
from Services.Generation.generator_service import generate_code
from Services.Storage.storage_service import put_object_to_s3, create_zip, create_url


def download_zip_code(event, context):
    """
    Lambda function to generate a code, put it into an S3 bucket, create a zip file,
    and return a URL pointing to the zip file.
    :param event: input event that triggers the Lambda function.
    :param context: context information about the execution environment.
    :return: a response containing the URL of the generated zip file.
    """
    json_data = json.loads(event['body'])
    code_generated = generate_code(json_data)
    response_put = put_object_to_s3(code_generated)
    create_zip()
    url = create_url()
    return {"body": json.dumps({"url": url})}
