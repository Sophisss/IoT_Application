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
from dal.dynamo_manager.base_aws_service import BaseAWSService
from dal.response_manager.response_manager import check_response_status
    """


def __generate_class() -> str:
    """
    This function generates the code for the DynamoDBManager class.
    :return: The code for the DynamoDBManager class.
    """
    return f"""
class BaseDynamoManager(BaseAWSService):
    dynamodb = None

    def __init__(self):
        BaseAWSService.__init__(self, "AWS DynamoDB")
        self.dynamodb = boto3.resource('dynamodb')

{generate_methods()}"""
