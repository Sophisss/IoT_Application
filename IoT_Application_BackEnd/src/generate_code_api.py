import json
import os
import boto3
from ruamel.yaml import YAML
import utilities
from generate_code_api_graphql import add_graphql_api_template
from generate_code_api_lambda import add_lambda_template
from generate_code_api_table import add_table_template

# Initialize the S3 client.
s3_client = boto3.client('s3')


# Function that generate the CloudFormation template.
def generate_template_api(bucket_name, folder_name):
    yaml = YAML()
    file_name = 'api.yaml'
    utilities.add_intestation_yaml_template(yaml, file_name, bucket_name, folder_name)
    return add_to_resources_template_api(yaml, file_name, bucket_name, folder_name)


# Function that update the api-related CloudFormation template with new resources.
def add_to_resources_template_api(yaml, file_name, bucket_name, folder_name):
    key = os.path.join(folder_name, file_name)
    template = yaml.load(utilities.get_s3_object(bucket_name, key)['Body'].read().decode('utf-8'))

    if 'Resources' not in template:
        template['Resources'] = {}

    json_data = utilities.read_json()
    add_lambda_template(json_data, template)
    add_table_template(json_data["awsConfig"]["dynamo"]["tables"], template)
    add_graphql_api_template(json_data, template)

    response = utilities.put_s3_object(bucket_name, key, yaml, template)

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {'statusCode': 200, 'body': 'File aggiornato con successo'}
    else:
        return {'statusCode': 500, 'body': json.dumps({
            'message': 'Errore durante l\'aggiornamento del file'
        })}


