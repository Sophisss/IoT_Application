from Services.Generation.Templates.cognito.generate_user_pool_template import generate_user_pool
from Services.Generation.Templates.generator_header_template_service import generate_header_template


def generate_cognito_template(json: dict) -> str:
    """
    This function generate the Cognito-related CloudFormation template.
    :param json: the JSON data.
    :return: the Cognito-related CloudFormation template.
    """
    return generate_template(json)


def generate_template(json):
    return f"""{generate_header_template()}
    """


def generate_resources(json):
    return f"""Resources:
    {generate_user_pool(json)}
    """
