from services.generation.templates.generator_graphql_template import generate_graphql_template
from services.generation.templates.generator_lambda_template import generate_lambda_template
from services.generation.templates.generator_table_template import generate_table_template
from services.generation.templates.header.generator_header_template import generate_header_template
from services.generation.templates.outputs.generator_graphql_output import generate_graphql_outputs


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
    {generate_lambda_template(json['entities'] + json['links'])}
    {generate_table_template(json['awsConfig']['dynamo']['tables'])}
    {generate_graphql_template(json['entities'] + json['links'])}
    """
