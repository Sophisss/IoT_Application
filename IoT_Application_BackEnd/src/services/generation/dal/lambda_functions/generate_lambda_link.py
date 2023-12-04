from services.generation.dal.lambda_functions.generate_lambda_definition import generate_lambda_definition
from services.generation.dal.lambda_functions.generate_case_link import generate_case_link
from services.generation.dal.lambda_functions.generate_exeption_lambda import generate_exception_lambda
from services.generation.dal.lambda_functions.generate_return_lambda import generate_return_lambda_link
from services.generation.dal.lambda_functions.generate_header_lambda import generate_header_lambda
from services.generation.dal.dynamo_manager.project_dynamo_manager.functions.utility import get_table_configuration


def generate_lambda_link(link, json):
    table = get_table_configuration(link['table'], json)
    name = f"{link['first_entity']}{link['second_entity']}"
    return f"""{generate_header_lambda(name)}
{generate_lambda_definition(f'{link["first_entity"]}_{link["second_entity"]}')}
{generate_case_link(link)}
{generate_exception_lambda()}
{generate_return_lambda_link(link['primary_key'][0], table['partition_key']['name'], link['primary_key'][1], table['sort_key']['name'])}
"""
