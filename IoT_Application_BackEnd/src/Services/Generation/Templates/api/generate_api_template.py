from Services.Generation.Templates.generator_header_template_service import generate_header_template


def generate_api_template(json: dict) -> str:
    """
    This function generates the api-related CloudFormation template.
    :param json: the JSON data.
    :return: the api-related CloudFormation template.
    """
    return f"""{generate_header_template()}
{generate_resources(json)}
        """


def generate_resources(json: dict) -> str:
    """
    This function generates the resources of the api-related CloudFormation template.
    :param json: the JSON data.
    :return: the resources of the api-related CloudFormation template.
    """
    return f"""Resources:
    """
