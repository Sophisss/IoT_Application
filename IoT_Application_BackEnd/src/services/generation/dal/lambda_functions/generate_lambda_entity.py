from services.generation.dal.lambda_functions.generate_case_entity import generate_case_entity
from services.generation.dal.lambda_functions.generate_header_lambda import generate_header
from services.generation.dal.lambda_functions.generate_lambda_definition import generate_lambda_definition
from services.generation.utility_methods import generate_resource_name


def generate_lambda_entity(entity, json_data):
    link = json_data['links']
    tables = json_data['awsConfig']['dynamo']['tables']
    return f"""{generate_header(generate_resource_name(entity), entity['table'], tables)}
{generate_lambda_definition(entity['name'])}
{generate_case_entity(entity, link)}
"""
