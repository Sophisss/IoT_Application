import json
import os
from io import BytesIO
import boto3
from ruamel.yaml import YAML

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


def add_intestation_yaml_template(yaml, file_name, bucket_name, folder_name):
    key = os.path.join(folder_name, file_name)
    template = yaml.load(get_s3_object(bucket_name, key)['Body'].read().decode('utf-8'))

    if template is None:
        template = {}

    new_resource = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Transform": "AWS::Serverless-2016-10-31",
        "Description": "Template",
        "Parameters": {
            "Project": {
                "Type": "String",
                "Description": "Name of the project"
            }
        },
        "Globals": {
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
    }

    template.update(new_resource)
    put_s3_object(bucket_name, key, yaml, template)


# Function that update the Cognito-related CloudFormation template with new resources.
def add_to_resources_template_cognito(yaml, file_name, bucket_name, folder_name):
    key = os.path.join(folder_name, file_name)
    template = yaml.load(get_s3_object(bucket_name, key)['Body'].read().decode('utf-8'))

    if 'Resources' not in template:
        template['Resources'] = {}

    json_data = read_json()
    json_data_cognito = json_data["awsConfig"]["authentication"]["cognito"]
    add_user_pool(json_data_cognito, template)
    add_identity_pool(json_data_cognito, template)

    response = put_s3_object(bucket_name, key, yaml, template)

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {'statusCode': 200, 'body': 'File aggiornato con successo'}
    else:
        return {'statusCode': 500, 'body': json.dumps({
            'message': 'Errore durante l\'aggiornamento del file'
        })}


# Function that add a User Pool to the CloudFormation template.
def add_user_pool(json_data, template):
    user_pool_name = json_data["UserPool"]["resource_name"]
    password_policy = json_data["UserPool"]["policy"]["PasswordPolicy"]
    new_resource = {
        f"{user_pool_name}": {
            "Type": "AWS::Cognito::UserPool",
            "Properties": {
                "UserPoolName": json_data["UserPool"]["UserPoolName"],
                "Policies": {
                    "PasswordPolicy": {
                        "MinimumLength": password_policy["MinimumLength"],
                        "RequireUppercase": password_policy["RequireUppercase"],
                        "RequireLowercase": password_policy["RequireLowercase"],
                        "RequireNumbers": password_policy["RequireNumbers"],
                        "RequireSymbols": password_policy["RequireSymbols"],
                        "TemporaryPasswordValidityDays": password_policy["TemporaryPasswordValidityDays"]
                    }
                },
                "LambdaConfig": {},
                "AutoVerifiedAttributes": ["email"],
                "UsernameAttributes": ["email"],
                "UserpoolTags": {
                    "Project": "!Ref Project"
                }
            }
        }
    }
    template['Resources'].update(new_resource)


# Function that add an Identity Pool to the CloudFormation template.
def add_identity_pool(json_data, template):
    identity_pool_name = json_data["IdentityPool"]["resource_name"]
    new_resource = {
        f"{identity_pool_name}": {
            "Type": "AWS::Cognito::IdentityPool",
            "Properties": {
                "IdentityPoolName": json_data["IdentityPool"]["IdentityPoolName"],
                "AllowUnauthenticatedIdentities": False,
                "CognitoIdentityProviders": [
                    {
                        "ProviderName": "!Ref UserPool"
                    }
                ],
                "ServerSideTokenCheck": False
            }
        }
    }
    template['Resources'].update(new_resource)


# Function that generate the CloudFormation template.
def generate_templates(file_name, bucket_name, folder_name):
    yaml = YAML()
    add_intestation_yaml_template(yaml, file_name, bucket_name, folder_name)
    return add_to_resources_template_cognito(yaml, file_name, bucket_name, folder_name)
