from services.generation.dal.lambda_function.generate_header_lambda import generate_header_lambda
from services.generation.dal.lambda_function.generate_lambda_definition import generate_lambda_definition
from services.generation.dal.lambda_function.generate_case_entity import generate_case_entity


def generate_lambda_entity(entity, link, tables):
    return f"""{generate_header_lambda(entity['name'], entity['table'], tables)}
{generate_lambda_definition(entity['name'])}
{generate_case_entity(entity, link)}
"""
