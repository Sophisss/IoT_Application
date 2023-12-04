from services.generation.dal.dynamo_manager.project_dynamo_manager.functions.utility import get_table_configuration
from services.generation.dal.lambda_functions.generate_header_lambda import generate_header_lambda
from services.generation.dal.lambda_functions.generate_lambda_definition import generate_lambda_definition
from services.generation.dal.lambda_functions.generate_case_entity import generate_case_entity
from services.generation.dal.lambda_functions.generate_exeption_lambda import generate_exception_lambda
from services.generation.dal.lambda_functions.generate_return_lambda import generate_return_lambda_entity


def generate_lambda_entity(entity, json):
    table = get_table_configuration(entity['table'], json)
    return f"""{generate_header_lambda(entity['name'])}
{generate_lambda_definition(entity['name'])}
{generate_case_entity(entity, json['links'], table['partition_key']['name'])}
{generate_exception_lambda()}
{generate_return_lambda_entity(entity['primary_key'][0], table['partition_key']['name'])}
"""
