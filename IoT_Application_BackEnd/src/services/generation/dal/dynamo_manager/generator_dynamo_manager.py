from services.generation.dal.dynamo_manager.generator_dynamo_manager_methods import generate_methods


def generate_dbmanager() -> str:
    """
    This function generates DynamoDBManager class.
    :return: The DynamoDBManager class generated.
    """
    return f"""{__generate_header()}
{__generate_class()}
"""


def __generate_header() -> str:
    """
    This function generates the header of the DynamoDBManager class.
    :return: The header of the DynamoDBManager class.
    """
    return """import boto3
from boto3.dynamodb.conditions import Key
    """


def __generate_class() -> str:
    """
    This function generates the code for the DynamoDBManager class.
    :return: The code for the DynamoDBManager class.
    """
    return f"""
class DynamoManager:
    dynamodb = boto3.resource('dynamodb')

{generate_methods()}"""



