from Services.Generation.Templates.cognito.generate_identity_pool_template import generate_identity_pool
from Services.Generation.Templates.cognito.generate_role_template import generate_role_template
from Services.Generation.Templates.cognito.generate_user_pool_template import generate_user_pool
from Services.Generation.Templates.header.generator_header_template_service import generate_header_template


def generate_cognito_template(json: dict) -> str:
    """
    This function generate the Cognito-related CloudFormation template.
    :param json: the JSON data.
    :return: the Cognito-related CloudFormation template.
    """
    return f"""{generate_header_template()}
{generate_resources(json)}
    """


def generate_resources(json: dict) -> str:
    """
    This function generate the resources of the Cognito-related CloudFormation template.
    :param json: the JSON data.
    :return: the resources of the Cognito-related CloudFormation template.
    """
    return f"""Resources:
    {generate_user_pool(json['UserPool'])}
    {generate_identity_pool(json['IdentityPool'])}
    {generate_role_template()}
    """
