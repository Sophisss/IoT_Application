from Services.Generation.Templates.header.generator_header_template_service import generate_header_template
from ..graphql_api.generate_graphql_template import generate_graphql_template
from ..outputs.graphql.generate_graphql_output import generate_graphql_outputs
from ..table.generate_table_template import generate_table_template
from ..lambda_template.generate_lambda_template import generate_lambda_template


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
