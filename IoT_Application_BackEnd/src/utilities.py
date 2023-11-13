import json
import boto3
import os
from io import BytesIO

# Initialize the S3 client.
s3_client = boto3.client('s3')


# Function that read JSON file and returns its content.
def read_json():
    with open('structure.json', 'r') as opened_file:
        return json.loads(opened_file.read())


# Function that retrieve the content of an S3 object.
def get_s3_object(bucket_name, key):
    return s3_client.get_object(Bucket=bucket_name, Key=key)


# Function that put an object in S3 bucket.
def put_s3_object(bucket_name, key, yaml, template):
    archive = BytesIO()
    yaml.dump(template, archive)
    archive.seek(0)
    return s3_client.put_object(Bucket=bucket_name, Key=key, Body=archive.read())


# Function that add the parameters to the CloudFormation template.
def add_parameters_template():
    return {
        "Project": {
            "Type": "String",
            "Description": "Name of the project"
        }
    }


# Function that add the globals to the CloudFormation template.
def add_globals_template():
    return {
        "Function": {
            "Timeout": 10,
            "Runtime": "python3.11",
            "CodeUri": "../src/",
            "MemorySize": 256,
            "Environment": {
                "Variables": {
                    "AWS_ACCOUNT_ID": "!Ref AWS::AccountId",
                    "AWS_REGION": "!Ref AWS::Region"
                }
            }
        }
    }


# Function that add the intestation to the CloudFormation template.
def add_intestation_yaml_template(yaml, file_name, bucket_name, folder_name):
    key = os.path.join(folder_name, file_name)
    template = yaml.load(get_s3_object(bucket_name, key)['Body'].read().decode('utf-8'))

    if template is None:
        template = {}

    new_resource = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Transform": "AWS::Serverless-2016-10-31",
        "Description": "Template",
        "Parameters": add_parameters_template(),
        "Globals": add_globals_template()
    }

    template.update(new_resource)
    put_s3_object(bucket_name, key, yaml, template)
