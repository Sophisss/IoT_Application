def generator_exception():
    """
    This function generates the exception file.
    :return: The exception file.
    """
    return f"""{generate_id_already_exists_error()}
{generate_item_not_present_error()}
{generate_entities_not_present_error()}
"""


def generate_id_already_exists_error():
    """
    This function generates the IdAlreadyExistsError class.
    :return: The IdAlreadyExistsError class.
    """
    return """class IdAlreadyExistsError(Exception):
    def __init__(self, name, id_value):
        self.message = f'{name} with the same id already exists'
        self.type = "IdAlreadyExistsError"
        super().__init__(self.message)
    """


def generate_item_not_present_error():
    """
    This function generates the ItemNotPresentError class.
    :return: The ItemNotPresentError class.
    """
    return """
class ItemNotPresentError(Exception):
    def __init__(self, name_entity, id_value):
        self.message = f'{name_entity} with the ID {id_value} is not in the database'
        self.type = 'ItemNotPresentError'
        super().__init__(self.message)
    """


def generate_entities_not_present_error():
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