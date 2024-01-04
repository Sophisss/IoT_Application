from services.generation.configuration_application.dal_resources.lambda_functions.resources.generator_case_link import generate_case_link
from services.generation.configuration_application.dal_resources.lambda_functions.resources.generator_exeption_lambda import \
    generate_exception_lambda
from services.generation.configuration_application.dal_resources.lambda_functions.resources.generator_header_lambda import \
    generate_header_lambda
from services.generation.configuration_application.dal_resources.lambda_functions.resources.generator_lambda_definition import \
    generate_lambda_definition
from services.generation.configuration_application.dal_resources.lambda_functions.resources.generator_return_lambda import \
    generate_return_lambda_link
from services.generation.utility_methods import generate_resource_name, get_table_configuration


def generate_lambda_link(link: dict, json: dict) -> str:
    """
    This method generates the lambda function for the link.
    :param link: link for which the lambda function is generated.
    :param json: JSON data.
    :return: the lambda function for the link.
    """
    table, link_name = __get_utility_resources(link, json)
    return f"""{generate_header_lambda(link_name,json['projectName'])}
{generate_lambda_definition(link_name ,json['projectName'])}
{generate_case_link(link)}
{generate_exception_lambda()}
{generate_return_lambda_link(link['primary_key'][0], table['partition_key']['name'], link['primary_key'][1], table['sort_key']['name'], table['parameters']['id_separator'])}
"""


def __get_utility_resources(link: dict, json: dict) -> tuple:
    """
    This method gets the utility resources for the link.
    :param link: link for which the utility resources are generated.
    :param json: JSON data.
    :return: the utility resources for the link.
    """
    table = get_table_configuration(link['table'], json)
    link_name = generate_resource_name(link)
    return table, link_name
