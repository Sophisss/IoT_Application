from services.generation.dal.lambda_function.generate_header_lambda import generate_header_lambda
from services.generation.dal.lambda_function.generate_lambda_definition import generate_lambda_definition
from services.generation.dal.lambda_function.generate_case_link import generate_case_link


def generate_lambda_link(link, tables, parameters):
    return f"""{generate_header_lambda(link['name'], link['table'], tables, parameters)}
{generate_lambda_definition(f'{link["first_entity"]}{link["second_entity"]}')}
{generate_case_link(link)}
"""
