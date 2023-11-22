from Services.Generation.DAL.DynamoClass.generate_create_entities_functions import generate_create_entities_functions
from Services.Generation.DAL.DynamoClass.generate_create_links_functions import generate_create_links_functions
from Services.Generation.DAL.DynamoClass.generate_delete_functions import generate_delete_functions
from Services.Generation.DAL.DynamoClass.generate_get_functions import generate_get_functions
from Services.Generation.DAL.DynamoClass.generate_utility_functions import generate_utility_functions
from Services.Generation.utility_methods import generate_resource_name


def generate_dbmanager(json: dict) -> str:
    """
    This function generates the code for the DynamoDBManager class.
    :param json: The json that contains the information.
    :return: The code for the DynamoDBManager class.
    """
    return f"""{__generate_header(json)}
{__generate_class(json)}
"""


def __generate_header(json: dict) -> str:
    """
    This function generates the header of the DynamoDBManager class.
    :return: The header of the DynamoDBManager class.
    """
    return f"""import boto3
from typing import Optional
from boto3.dynamodb.conditions import Key
from ExceptionClasses import IdAlreadyExistsError
{__generate_header_entities(json['entities'])}
{__generate_header_links(json['links'])}
    """


def __generate_header_entities(entities: list) -> str:
    """
    This function generates the header for the entities.
    :param entities: The entities that are needed to generate the header.
    :return: The header for the entities.
    """
    returns = ""
    for entity in entities:
        entity_name = generate_resource_name(entity)
        returns += f"from Model.{entity_name} import {entity_name}\n"
    return returns


def __generate_header_links(links: list) -> str:
    """
    This function generates the header for the links.
    :param links: The links that are needed to generate the header.
    :return: The header for the links.
    """
    returns = ""
    for link in links:
        link_name = generate_resource_name(link)
        returns += f"from Model.{link_name} import {link_name}\n"
    return returns


def __generate_class(json: dict) -> str:
    """
    This function generates the code for the DynamoDBManager class.
    :param json: The json that contains the information.
    :return: The code for the DynamoDBManager class.
    """
    return f"""
class DynamoDBManager:
{__generate_constructor()}
{generate_create_entities_functions(json['entities'])}
{generate_create_links_functions(json['links'])}
{generate_delete_functions(json)}
{generate_get_functions()}
{generate_utility_functions()}"""


def __generate_constructor() -> str:
    """
    This function generates the code for the constructor of the DynamoDBManager class.
    :return: The code for the constructor of the DynamoDBManager class.
    """
    return """    def __init__(self, table_name, separator, partition_key_table, sort_key_table, single_entity_storage_keyword, gsi):
        self._dynamodb = boto3.resource('dynamodb')
        self._table = self._dynamodb.Table(table_name)
        self._separator = separator
        self._partition_key_table = partition_key_table
        self._sort_key_table = sort_key_table
        self._single_entity_storage_keyword = single_entity_storage_keyword
        self._GSI = gsi
    """
