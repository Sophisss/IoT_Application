from services.generation.configuration_application.template_resources.api.resources.generator_graphql_template import \
    generate_graphql_template
from services.generation.configuration_application.template_resources.api.resources.generator_lambda_template import \
    generate_lambda_template
from services.generation.configuration_application.template_resources.api.resources.generator_roles_and_policies import \
    generate_roles_and_policies
from services.generation.configuration_application.template_resources.api.resources.generator_table_template import \
    generate_table_template
from services.generation.configuration_application.template_resources.api.resources.generator_header_template import \
    generate_header_template
from services.generation.configuration_application.template_resources.outputs.generator_graphql_output import \
    generate_graphql_outputs


def generate_api_template(json: dict) -> str:
    """
    This function generates the api-related CloudFormation template.
    :param json: the JSON data.
    :return: the api-related CloudFormation template.
    """
    return f"""{generate_header_template()}
{__generate_resources(json)}

Outputs:
{generate_graphql_outputs()}
    """


def __generate_resources(json: dict) -> str:
    """
    This function generate the resources of the api-related CloudFormation template.
    :param json: the JSON data.
    :return: the resources of the api-related CloudFormation template.
    """
    return f"""Resources:
    {__generate_entity_link_resources(json['entities'] + json['links'])}
    {__generate_tables_resources(json['awsConfig']['dynamo']['tables'])}
    """


def __generate_tables_resources(tables: list) -> str:
    """
    This function generates the tables resources of the api-related CloudFormation template.
    :param tables: the list of tables.
    :return: the tables resources of the api-related CloudFormation template.
    """
    return f"""{generate_table_template(tables)}
{generate_roles_and_policies(tables)}
    """


def __generate_entity_link_resources(resources: list) -> str:
    """
    This function generates the entity and link resources of the api-related CloudFormation template.
    :param resources: the list of resources.
    :return: the entity and link resources of the api-related CloudFormation template.
    """
    return f"""{generate_lambda_template(resources)}
{generate_graphql_template(resources)}
    """
