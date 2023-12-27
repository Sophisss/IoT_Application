from services.generation.configuration_application.dal.dynamo_manager.project_dynamo_manager.functions.utility import \
    get_table_configuration
from services.generation.configuration_application.dal.lambda_functions.generate_case_entity import generate_case_entity
from services.generation.configuration_application.dal.lambda_functions.generate_exeption_lambda import \
    generate_exception_lambda
from services.generation.configuration_application.dal.lambda_functions.generate_header_lambda import \
    generate_header_lambda
from services.generation.configuration_application.dal.lambda_functions.generate_lambda_definition import \
    generate_lambda_definition
from services.generation.configuration_application.dal.lambda_functions.generate_return_lambda import \
    generate_return_lambda_entity
from services.generation.utility_methods import generate_resource_name


def generate_lambda_entity(entity, json):
    table = get_table_configuration(entity['table'], json)
    name = generate_resource_name(entity)
    return f"""{generate_header_lambda(name, json['projectName'])}
{generate_lambda_definition(name, json['projectName'])}
{generate_case_entity(entity, json['links'], table['partition_key']['name'], table['parameters']['id_separator'])}
{generate_exception_lambda()}
{generate_return_lambda_entity(entity['primary_key'][0], table['partition_key']['name'], table['parameters']['id_separator'])}
"""
