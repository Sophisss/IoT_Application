import os
from utility_methods import get_s3_object, put_s3_object, create_archive


def add_header_yaml_template(yaml, file_name, bucket_name, folder_name):
    """
    This function add the header to the CloudFormation template.
    :param yaml: YAML object.
    :param file_name: File name.
    :param bucket_name: S3 bucket name.
    :param folder_name: S3 folder name.
    """
    key = os.path.join(folder_name, file_name)
    template = yaml.load(get_s3_object(bucket_name, key)['Body'].read().decode('utf-8'))

    if template is None:
        template = {}

    template.update(create_template_header())
    put_s3_object(bucket_name, key, create_archive(yaml, template))


def create_template_header():
    """
    This function create the header of the CloudFormation template.
    :return: Template header.
    """
    return {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Transform": "AWS::Serverless-2016-10-31",
        "Description": "Template",
        "Parameters": add_parameters_template(),
        "Globals": add_globals_template()
    }


def add_parameters_template():
    """
    This function add the parameters to the CloudFormation template.
    :return: Parameters.
    """
    return {
        "Project": {
            "Type": "String",
            "Description": "Name of the project"
        }
    }


def add_globals_template():
    """
    This function add the globals to the CloudFormation template.
    :return: Globals.
    """
    return {
        "Function": {
            "Timeout": 10,
            "Runtime": "python3.11",
            "CodeUri": "../src/",
            "MemorySize": 256,
            "Environment": {
                "Variables": {
                    "AWS_ACCOUNT_ID": {"Fn::Ref": "AWS::AccountId"},
                    "AWS_REGION": {"Fn::Ref": "AWS::Region"}
                }
            }
        }
    }
