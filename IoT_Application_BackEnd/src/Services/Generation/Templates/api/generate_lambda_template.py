from Services.Generation.Templates.api.generate_api_template import generate_api_template
from Services.Generation.Templates.generator_header_template_service import generate_header_template


def generate_lambda_template(json: dict) -> str:
    """
    This function generates the lambda-related CloudFormation template.
    :param json: the JSON data.
    :return: the lambda-related CloudFormation template.
    """
    return f"""{generate_header_template()}
{generate_resources(json)}
    """


def generate_resources(json: dict) -> str:
    """
    This function generate the resources of the lambda-related CloudFormation template.
    :param json: the JSON data.
    :return: the resources of the lambda-related CloudFormation template.
    """
    return f"""Resources:
    {generate_api_template(json)}
    """
