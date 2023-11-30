def generator_exception() -> str:
    """
    This function generates the exception file.
    :return: The exception file.
    """
    return f"""{__generate_id_already_exists_error()}
{__generate_item_not_present_error()}
{__generate_internal_server_error()}
{__generate_invalid_api_error()}
"""


def __generate_id_already_exists_error() -> str:
    """
    This function generates the IdAlreadyExistsError class.
    :return: The IdAlreadyExistsError class.
    """
    return """class IdAlreadyExistsError(Exception):
    def __init__(self):
        self.message = f'Item with the same id already exists'
        self.type = "IdAlreadyExistsError"
        super().__init__(self.message)
    """


def __generate_item_not_present_error() -> str:
    """
    This function generates the ItemNotPresentError class.
    :return: The ItemNotPresentError class.
    """
    return """
class ItemNotPresentError(Exception):
    def __init__(self):
        self.message = 'Item/s not present'
        self.type = "ItemNotPresentError"
        super().__init__(self.message)
    """


def __generate_internal_server_error() -> str:
    """
    This function generates the InternalServerError class.
    :return: The InternalServerError class.
    """
    return """
class InternalServerError(Exception):
    def __init__(self):
        self.message = "Internal Server Error"
        self.type = 'InternalServerError'
        super().__init__(self.message)
        """


def __generate_invalid_api_error() -> str:
    """
    This function generates the InvalidApiError class.
    :return: The InvalidApiError class.
    """
    return """
class InvalidApiError(Exception):
    def __init__(self, api_name):
        self.message = f"Invalid api {api_name}"
        self.type = 'InvalidApiError'
        super().__init__(self.message)
    """
