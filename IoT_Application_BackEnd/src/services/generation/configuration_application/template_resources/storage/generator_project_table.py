from services.generation.configuration_application.template_resources.generator_header_template import generate_header_template
from services.generation.configuration_application.template_resources.storage.resources.generator_timestream_template import generate_timestream_template
from services.generation.configuration_application.template_resources.storage.resources.generator_dynamo_table_template import generate_dynamo_table_template


def generate_project_table(json: dict) -> str:
    """
    This method generates the CloudFormation template for the table resources of the project.
    :param json: The JSON object that contains the configuration of the project.
    :return: The CloudFormation template for the table resources of the project.
    """
    return f"""{generate_header_template()}
    
Resources:
{generate_dynamo_table_template(json)}
{generate_timestream_template(json)}
    """
