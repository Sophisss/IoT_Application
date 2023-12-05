from services.generation.dal.dynamo_manager.project_dynamo_manager.functions.generator_entity_functions import generate_entity_methods
from services.generation.dal.dynamo_manager.project_dynamo_manager.functions.generator_link_functions import generate_link_methods
from services.generation.utility_methods import generate_resource_name


def generator_project_dynamo_manager(json_data: dict) -> str:
    """
    This method generates a DynamoDB manager class for the project based on the provided JSON schema.
    :param json_data: The JSON schema containing information.
    :return: The generated DynamoDB manager class.
    """
    return f"""{__generate_header(json_data)}
{__generate_class(json_data)}
    """


def __generate_header(json_data: dict) -> str:
    """
    This method generates the header of the DynamoDB manager class.
    :param json_data: The JSON schema containing information.
    :return: The header of the DynamoDB manager class.
    """
    return f"""from boto3.dynamodb.conditions import Key
from dal.dynamo_manager.dynamo_manager import BaseDynamoManager
from dal.response_manager.exception_class import ItemNotPresentError
from dal.utility import remove_null_values
{__generate_header_entities_and_links(json_data['entities'] + json_data['links'])}
    """


def __generate_header_entities_and_links(json_data: dict) -> str:
    """
    This method generates the header of the entities and links of the DynamoDB manager class.
    :param json_data: The JSON schema containing information.
    :return: The header of the entities and links of the DynamoDB manager class.
    """
    return "".join(map(lambda item: __create_header(generate_resource_name(item)), json_data))


def __create_header(item_name: str) -> str:
    """
    This method generates the header of the entity or link of the DynamoDB manager class.
    :param item_name: The name of the entity or link.
    :return: The header of the entity or link of the DynamoDB manager class.
    """
    return f"""from model.{item_name.lower()} import {item_name}
"""


def __generate_class(json_data: dict) -> str:
    """
    This method generates the class of the DynamoDB manager class.
    :param json_data: The JSON schema containing information.
    :return: The class of the DynamoDB manager class.
    """
    return f"""class {json_data['projectName']}DynamoManager(BaseDynamoManager):
{generate_methods(json_data)}
    """


def generate_methods(json_data: dict) -> str:
    """
    This method generates the methods of the DynamoDB manager class.
    :param json_data: The JSON schema containing information.
    :return: The methods of the DynamoDB manager class.
    """
    return ("".join(map(lambda entity: generate_entity_methods(entity, json_data), json_data['entities'])) +
            "".join(map(lambda link: generate_link_methods(link, json_data), json_data['links'])))
