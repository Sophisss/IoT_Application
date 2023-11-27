def generator_exception() -> str:
    """
    This function generates the exception file.
    :return: The exception file.
    """
    return f"""{__generate_id_already_exists_error()}
{__generate_item_not_present_error()}
{__generate_entities_not_present_error()}
"""


def __generate_id_already_exists_error() -> str:
    """
    This function generates the IdAlreadyExistsError class.
    :return: The IdAlreadyExistsError class.
    """
    return """class IdAlreadyExistsError(Exception):
    def __init__(self, name):
        self.message = f'{name} with the same id already exists'
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
        self.message = 'Item with the same id already exists'
        self.type = "IdAlreadyExistsError"
        super().__init__(self.message)
    """


def __generate_entities_not_present_error() -> str:
    """
    This function generates the EntitiesNotPresentError class.
    :return: The EntitiesNotPresentError class.
    """
    return """
class EntitiesNotPresentError(Exception):
    def __init__(self, name_entity):
        self.message = f' No entities with name {name_entity} '
        self.type = 'ItemNotPresentError'
        super().__init__(self.message)
    """