def generate_response_manager() -> str:
    """
    This function generates the response manager.
    :return: The response manager.
    """
    return f"""from dal.response_manager.exception_class import InternalServerError, ItemNotPresentError
    
{__generate_check_response_status_method()}
{__generate_check_response_item_method()}
    """


def __generate_check_response_status_method() -> str:
    """
    This function generates the check_response_status method.
    :return: The check_response_status method.
    """
    return """
def check_response_status(response: dict):
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise InternalServerError()
"""


def __generate_check_response_item_method() -> str:
    """
    This function generates the check_response_item method.
    :return: The check_response_item method.
    """
    return """
def check_response_item(response: dict):
    if not response:
        raise ItemNotPresentError()"""
