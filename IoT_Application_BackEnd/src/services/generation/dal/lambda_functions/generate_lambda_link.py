from services.generation.dal.lambda_functions.generate_case_link import generate_case_link
from services.generation.dal.lambda_functions.generate_header_lambda import generate_header
from services.generation.dal.lambda_functions.generate_lambda_definition import generate_lambda_definition

from services.generation.utility_methods import generate_resource_name


def generate_lambda_link(link, json_data: dict) -> str:
    return f"""{generate_header(generate_resource_name(link), link['table'], json_data['awsConfig']['dynamo']['tables'])}
{generate_lambda_definition(f'{link["first_entity"]}{link["second_entity"]}')}
{generate_case_link(link)}
"""
