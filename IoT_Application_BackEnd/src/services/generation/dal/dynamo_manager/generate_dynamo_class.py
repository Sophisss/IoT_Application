from services.generation.dal.dynamo_manager.functions.generate_create_functions import generate_create_functions
from services.generation.dal.dynamo_manager.functions.generate_delete_functions import generate_delete_functions
from services.generation.dal.dynamo_manager.functions.generate_get_functions import generate_get_functions
from services.generation.dal.dynamo_manager.functions.generate_update_functions import generate_update_functions
from services.generation.dal.dynamo_manager.functions.generate_utility_functions import generate_utility_functions


def generate_dbmanager(json: dict) -> str:
    """
    This function generates the code for the DynamoDBManager class.
    :param json: The json that contains the information.
    :return: The code for the DynamoDBManager class.
    """
    return f"""{__generate_header()}
{__generate_class(json)}
"""


def __generate_header() -> str:
    """
    This function generates the header of the DynamoDBManager class.
    :return: The header of the DynamoDBManager class.
    """
    return f"""from typing import Optional
from boto3.dynamodb.conditions import Key
from exception_class import IdAlreadyExistsError, ItemNotPresentError
from configuration import Configuration
    """


def __generate_class(json: dict) -> str:
    """
    This function generates the code for the DynamoDBManager class.
    :param json: The json that contains the information.
    :return: The code for the DynamoDBManager class.
    """
    return f"""
class DynamoManager:
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
    return """    def __init__(self, configuration: Configuration):
        self.configuration = configuration"""
