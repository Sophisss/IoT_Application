import os
import utility_methods as utilities
from ruamel.yaml import YAML
from generate_code_api_graphql import add_graphql_api_template
from generate_code_api_lambda import add_lambda_template
from generate_code_api_table import add_table_template
from generate_header_templates import add_header_yaml_template


def generate_template_api(bucket_name, folder_name):
    """
    This function generate the CloudFormation template.
    :param bucket_name: S3 bucket name.
    :param folder_name: S3 folder name.
    """
    yaml = YAML()
    yaml.indent(offset=2, sequence=4, mapping=2)
    file_name = 'api.yaml'
    add_header_yaml_template(yaml, file_name, bucket_name, folder_name)
    return add_to_resources_template_api(yaml, file_name, bucket_name, folder_name)


def add_to_resources_template_api(yaml, file_name, bucket_name, folder_name):
    """
    This function update the CloudFormation template with new resources.
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
    This function add new resources to the CloudFormation template.
    :param template: CloudFormation template.
    """
    if 'Resources' not in template:
        template['Resources'] = {}

    json_data = utilities.read_json()
    add_lambda_template(json_data, template)
    add_table_template(json_data["awsConfig"]["dynamo"]["tables"], template)
    add_graphql_api_template(json_data, template)
