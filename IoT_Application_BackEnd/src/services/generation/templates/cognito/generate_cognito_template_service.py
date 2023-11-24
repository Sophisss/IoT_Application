from services.generation.templates.cognito.resources.generate_client_template import generate_client
from services.generation.templates.cognito.resources.generate_user_pool_template import generate_user_pool
from services.generation.templates.header.generator_header_template_service import generate_header_template
from services.generation.templates.outputs.userpool.generate_userpool_outputs import generate_user_pool_outputs


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
