from services.generation.dal.dynamo_manager.functions.generate_create_functions import generate_create_functions
from services.generation.dal.dynamo_manager.functions.generate_delete_functions import generate_delete_functions
from services.generation.dal.dynamo_manager.functions.generate_get_functions import generate_get_functions
from services.generation.dal.dynamo_manager.functions.generate_update_functions import generate_update_functions


def generate_dbmanager(json: dict) -> str:
    """
    This function generates DynamoDBManager class.
    :param json: The json that contains the information.
    :return: The DynamoDBManager class generated.
    """
    return f"""{__generate_header()}
{__generate_class(json)}
"""


def __generate_header() -> str:
    """
    This function generates the header of the DynamoDBManager class.
    :return: The header of the DynamoDBManager class.
    """
    return f"""from boto3.dynamodb.conditions import Key
from utility.exception_class import IdAlreadyExistsError, ItemNotPresentError
from configuration import Configuration
from utility.utility import *
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
{__generate_methods(json)}"""


def __generate_constructor() -> str:
    """
    This function generates the code for the constructor of the DynamoDBManager class.
    :return: The code for the constructor of the DynamoDBManager class.
    """
    return """    def __init__(self, configuration: Configuration):
        self.configuration = configuration"""


def __generate_methods(json: dict) -> str:
    """
    This function generates the code for the methods of the DynamoDBManager class.
    :param json: The json that contains the information.
    :return: The code for the methods of the DynamoDBManager class.
    """
    return f"""{generate_create_functions(json)}
{generate_delete_functions(json)}
{generate_update_functions(json)}
{generate_get_functions()}"""
