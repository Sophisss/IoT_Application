from services.generation.dal.dynamo_manager.generate_create_functions import generate_create_functions
from services.generation.dal.dynamo_manager.generate_delete_functions import generate_delete_functions
from services.generation.dal.dynamo_manager.generate_get_functions import generate_get_functions
from services.generation.dal.dynamo_manager.generate_update_functions import generate_update_functions
from services.generation.dal.dynamo_manager.generate_utility_functions import generate_utility_functions


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
from ExceptionClasses import IdAlreadyExistsError, ItemNotPresentError
    """


def __generate_class(json: dict) -> str:
    """
    This function generates the code for the DynamoDBManager class.
    :param json: The json that contains the information.
    :return: The code for the DynamoDBManager class.
    """
    return f"""class DynamoDBManager:
{__generate_constructor()}
{generate_create_functions(json)}
{generate_delete_functions(json)}
{generate_update_functions(json)}
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
        self._GSI = gsi"""
