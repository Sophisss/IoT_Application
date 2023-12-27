from services.generation.configuration_application.dal_resources.lambda_functions.resources.generator_case_entity import generate_case_entity
from services.generation.configuration_application.dal_resources.lambda_functions.resources.generator_exeption_lambda import \
    generate_exception_lambda
from services.generation.configuration_application.dal_resources.lambda_functions.resources.generator_header_lambda import \
    generate_header_lambda
from services.generation.configuration_application.dal_resources.lambda_functions.resources.generator_lambda_definition import \
    generate_lambda_definition
from services.generation.configuration_application.dal_resources.lambda_functions.resources.generator_return_lambda import \
    generate_return_lambda_entity
from services.generation.utility_methods import generate_resource_name, get_table_configuration


def generate_lambda_entity(entity: dict, json: dict) -> str:
    """
    This function generates the lambda function for the entity.
    :param entity: entity for which the lambda function is generated.
    :param json: JSON data.
    :return: the lambda function for the entity.
    """
    table = get_table_configuration(entity['table'], json)
    name = generate_resource_name(entity)
    return f"""{generate_header_lambda(name, json['projectName'])}
{generate_lambda_definition(name, json['projectName'])}
{generate_case_entity(entity, json['links'], table['partition_key']['name'], table['parameters']['id_separator'])}
{generate_exception_lambda()}
{generate_return_lambda_entity(entity['primary_key'][0], table['partition_key']['name'], table['parameters']['id_separator'])}
"""
