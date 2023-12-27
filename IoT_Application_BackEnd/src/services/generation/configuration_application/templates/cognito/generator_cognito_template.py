from services.generation.configuration_application.templates.cognito.resources.generator_client_template import \
    generate_client
from services.generation.configuration_application.templates.cognito.resources.generator_user_pool_template import \
    generate_user_pool
from services.generation.configuration_application.templates.header.generator_header_template import \
    generate_header_template
from services.generation.configuration_application.templates.outputs.generator_userpool_outputs import \
    generate_user_pool_outputs


def generate_cognito_template(json: dict) -> str:
    """
    This function generate the Cognito-related CloudFormation template.
    :param json: the JSON data.
    :return: the Cognito-related CloudFormation template.
    """
    return f"""{generate_header_template()}
{__generate_resources(json)}

Outputs: 
{generate_user_pool_outputs()}
    """


def __generate_resources(json: dict) -> str:
    """
    This function generate the resources of the Cognito-related CloudFormation template.
    :param json: the JSON data.
    :return: the resources of the Cognito-related CloudFormation template.
    """
    return f"""Resources:
    {generate_user_pool(json['UserPool'])}
    {generate_client()}
    """
