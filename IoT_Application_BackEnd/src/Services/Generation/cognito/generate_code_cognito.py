import os
from ruamel.yaml import YAML
import utility_methods as utilities
from generate_header_templates import add_header_yaml_template


def generate_template_cognito(bucket_name, folder_name):
    """
    This function generate the Cognito-related CloudFormation template.
    :param bucket_name: S3 bucket name.
    :param folder_name: S3 folder name.
    :return: the Cognito-related CloudFormation template.
    """
    yaml = YAML()
    file_name = 'permissions.yaml'
    add_header_yaml_template(yaml, file_name, bucket_name, folder_name)
    return add_to_resources_template_cognito(yaml, file_name, bucket_name, folder_name)


def add_to_resources_template_cognito(yaml, file_name, bucket_name, folder_name):
    """
    This function update the Cognito-related CloudFormation template with new resources.
    :param yaml: YAML object.
    :param file_name: File name.
    :param bucket_name: S3 bucket name.
    :param folder_name: S3 folder name.
    :return: Response.
    """
    key = os.path.join(folder_name, file_name)
    template = yaml.load(utilities.get_s3_object(bucket_name, key)['Body'].read().decode('utf-8'))
    add_resources_to_template(template)

    response = utilities.put_s3_object(bucket_name, key, utilities.create_archive(yaml, template))
    return utilities.handle_response(response, 'File updated successfully')


def add_resources_to_template(template):
    """
    This function add new resources to the Cognito-related CloudFormation template.
    :param template: Cognito-related CloudFormation template.
    """
    if 'Resources' not in template:
        template['Resources'] = {}

    json_data = utilities.read_json()
    json_data_cognito = json_data["awsConfig"]["authentication"]["cognito"]
    add_user_pool(json_data_cognito, template)
    add_identity_pool(json_data_cognito, template)


def add_user_pool(json_data, template):
    """
    This function add a User Pool to the CloudFormation template.
    :param json_data: the json data of the configuration file.
    :param template: the CloudFormation template.
    """
    user_pool_name = json_data["UserPool"]["resource_name"]
    password_policy = json_data["UserPool"]["policy"]["PasswordPolicy"]
    template['Resources'][f"{user_pool_name}"] = {
        "Type": "AWS::Cognito::UserPool",
        "Properties": add_properties_user_pool_template(json_data, password_policy)
    }


def add_properties_user_pool_template(json_data, password_policy):
    """
    This function add the properties of the user pool to the CloudFormation template.
    :param json_data: the json data of the configuration file.
    :param password_policy: the password policy of the user pool.
    :return: the properties of the user pool.
    """
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


def add_policies_template(password_policy):
    """
    This function add the policies of the user pool to the CloudFormation template.
    :param password_policy: the password policy of the user pool.
    :return: the policies of the user pool.
    """
    return {
        "PasswordPolicy": add_password_policy_template(password_policy)
    }


def add_password_policy_template(password_policy):
    """
    This function add the password policy to the CloudFormation template.
    :param password_policy: the password policy of the user pool.
    :return: the password policy of the user pool.
    """
    return {
        "MinimumLength": password_policy["MinimumLength"],
        "RequireUppercase": password_policy["RequireUppercase"],
        "RequireLowercase": password_policy["RequireLowercase"],
        "RequireNumbers": password_policy["RequireNumbers"],
        "RequireSymbols": password_policy["RequireSymbols"],
        "TemporaryPasswordValidityDays": password_policy["TemporaryPasswordValidityDays"]
    }


def add_identity_pool(json_data, template):
    """
    This function add an Identity Pool to the CloudFormation template.
    :param json_data: the json data of the configuration file.
    :param template: the CloudFormation template.
    """
    identity_pool_name = json_data["IdentityPool"]["resource_name"]
    template['Resources'][f"{identity_pool_name}"] = {
        "Type": "AWS::Cognito::IdentityPool",
        "Properties": add_properties_identity_pool_template(json_data)
    }


def add_properties_identity_pool_template(json_data):
    """
    This function add the identity pool properties to the CloudFormation template.
    :param json_data: the json data of the configuration file.
    :return: the identity pool properties.
    """
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




