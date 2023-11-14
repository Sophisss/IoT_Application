import json
import os
import boto3
from ruamel.yaml import YAML
import utility_methods

# Initialize the S3 client.
s3_client = boto3.client('s3')


# Function that update the Cognito-related CloudFormation template with new resources.
def add_to_resources_template_cognito(yaml, file_name, bucket_name, folder_name):
    key = os.path.join(folder_name, file_name)
    template = yaml.load(utilities.get_s3_object(bucket_name, key)['Body'].read().decode('utf-8'))

    if 'Resources' not in template:
        template['Resources'] = {}

    json_data = utilities.read_json()
    json_data_cognito = json_data["awsConfig"]["authentication"]["cognito"]
    add_user_pool(json_data_cognito, template)
    add_identity_pool(json_data_cognito, template)

    response = utilities.put_s3_object(bucket_name, key, yaml, template)

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {'statusCode': 200, 'body': 'File aggiornato con successo'}
    else:
        return {'statusCode': 500, 'body': json.dumps({
            'message': 'Errore durante l\'aggiornamento del file'
        })}


# Function that add the user pool properties to the CloudFormation template.
def add_properties_userpool_template(json_data, password_policy):
    return {
        "UserPoolName": json_data["UserPool"]["UserPoolName"],
        "Policies": add_policies_template(password_policy),
        "LambdaConfig": {},
        "AutoVerifiedAttributes": ["email"],
        "UsernameAttributes": ["email"],
        "UserpoolTags": {
            "Project": "!Ref Project"
        }
    }


# Function that add the policies to the CloudFormation template.
def add_policies_template(password_policy):
    return {
        "PasswordPolicy": add_password_policy_template(password_policy)
    }


# Function that add the password policy to the CloudFormation template.
def add_password_policy_template(password_policy):
    return {
        "MinimumLength": password_policy["MinimumLength"],
        "RequireUppercase": password_policy["RequireUppercase"],
        "RequireLowercase": password_policy["RequireLowercase"],
        "RequireNumbers": password_policy["RequireNumbers"],
        "RequireSymbols": password_policy["RequireSymbols"],
        "TemporaryPasswordValidityDays": password_policy["TemporaryPasswordValidityDays"]
    }


# Function that add a User Pool to the CloudFormation template.
def add_user_pool(json_data, template):
    user_pool_name = json_data["UserPool"]["resource_name"]
    password_policy = json_data["UserPool"]["policy"]["PasswordPolicy"]
    new_resource = {
        f"{user_pool_name}": {
            "Type": "AWS::Cognito::UserPool",
            "Properties": add_properties_userpool_template(json_data, password_policy)
        }
    }
    template['Resources'].update(new_resource)


# Function that add the identity pool properties to the CloudFormation template.
def add_properties_identitypool_template(json_data):
    return {
        "IdentityPoolName": json_data["IdentityPool"]["IdentityPoolName"],
        "AllowUnauthenticatedIdentities": False,
        "CognitoIdentityProviders": [
            {
                "ProviderName": "!Ref UserPool"
            }
        ],
        "ServerSideTokenCheck": False
    }


# Function that add an Identity Pool to the CloudFormation template.
def add_identity_pool(json_data, template):
    identity_pool_name = json_data["IdentityPool"]["resource_name"]
    new_resource = {
        f"{identity_pool_name}": {
            "Type": "AWS::Cognito::IdentityPool",
            "Properties": add_properties_identitypool_template(json_data)
        }
    }
    template['Resources'].update(new_resource)


# Function that generate the CloudFormation template.
def generate_template_cognito(bucket_name, folder_name):
    yaml = YAML()
    file_name = 'permissions.yaml'
    utilities.add_header_yaml_template(yaml, file_name, bucket_name, folder_name)
    return add_to_resources_template_cognito(yaml, file_name, bucket_name, folder_name)
