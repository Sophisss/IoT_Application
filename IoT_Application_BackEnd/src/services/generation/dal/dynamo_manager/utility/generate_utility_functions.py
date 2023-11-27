def generate_utility_functions() -> str:
    """
    This function generates the code for the utility functions.
    :return: The code for the utility functions.
    """
    return f"""from typing import Optional
    
{__generate_create_id()}
{__generate_remove_values()}
{__generate_create_arguments()}
{__generate_update_expression()}
{__generate_create_expression_attribute_values()}
{__generate_get_attr()}
    """


def __generate_create_id() -> str:
    """
    This function generates the code for the create_id function.
    :return: The code for the create_id function.
    """
    return """
def create_id(object_name: str, object_id: str, separator: str) -> str:
    return f"{object_name}{separator}{object_id}"
    """


def __generate_remove_values() -> str:
    """
    This function generates the code for the remove_null_values function.
    :return: The code for the remove_null_values function.
    """
    return """
def remove_values(dictionary: dict, keys_to_remove: list) -> dict:
    return {
        key: remove_values(value, keys_to_remove) if isinstance(value, dict) else value
        for key, value in dictionary.items()
        if value is not None and key not in keys_to_remove
    }
    """


def __generate_create_arguments() -> str:
    """
    This function generates the code for the create_arguments function.
    :return: The code for the create_arguments function.
    """
    return """
def create_arguments(single_entity_storage_keyword: str, partition_key_table: str, sort_key_table: str,
                     id_first_entity: str, id_second_entity=None) -> dict:
    return {
        partition_key_table: id_first_entity,
        sort_key_table: single_entity_storage_keyword if id_second_entity is None else id_second_entity
    }
    """


def __generate_update_expression() -> str:
    """
    This function generates the code for the update_expression function.
    :return: The code for the update_expression function.
    """
    return """
def create_update_expression(arguments: dict) -> str:
    return 'SET ' + ', '.join([f'{key} = :{key}' for key in arguments.keys()])
    """


def __generate_create_expression_attribute_values() -> str:
    """
    This function generates the code for the create_expression_attribute_values function.
    :return: The code for the create_expression_attribute_values function.
    """
    return """
def create_expression_attribute_values(arguments: dict) -> dict:
    return {f':{key}': value for key, value in arguments.items()}
    """


def __generate_get_attr() -> str:
    """
    This function generates the code for the get_attr function.
    :return: The code for the get_attr function.
    """
    return """
def getAttr(object_to_get_attr, id_key: Optional[str] = None):
    return getattr(object_to_get_attr, id_key) if id_key is not None else None"""