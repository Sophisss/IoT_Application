def generate_base_aws_service() -> str:
    """
    This method generates the base AWS service class.
    :return: The base AWS service class.
    """
    return """class BaseAWSService:

    __service_name: str

    # Response parsing keys
    METADATA = "ResponseMetadata"
    STATUS_CODE = "HTTPStatusCode"
    ITEMS = "Items"
    ITEM = "Item"

    LAST_EVALUATED_KEY = "LastEvaluatedKey"

    def __init__(self, name: str):
        self.__service_name = name

    def validate_aws_response(self, response: dict, action: str):
        if not isinstance(response, dict) or self.METADATA not in response:
            raise Exception(self.__service_name + " " + action + " invalid response")

        metadata = response.get(self.METADATA)
        if not isinstance(metadata, dict) or self.STATUS_CODE not in metadata or metadata.get(self.STATUS_CODE) != 200:
            raise Exception(self.__service_name + " " + action + " invalid response " + str(metadata))
    """