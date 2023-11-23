def generate_utility_functions() -> str:
    return f"""{__generate_create_id()}
{__generate_remove_null_values()}
{__generate_create_arguments()}
{__generate_update_expression()}
{__generate_create_expression_attribute_values()}
    """


def __generate_create_id() -> str:
    """
    This function generates the code for the create_id function.
    :return: The code for the create_id function.
    """
    return """
    def create_id(self, name: str, object_id: str) -> str:
        return f"{name}{self._separator}{object_id}"
    """


def __generate_remove_null_values() -> str:
    """
    This function generates the code for the remove_null_values function.
    :return: The code for the remove_null_values function.
    """
    return """
    def __remove_null_values(self, dictionary: dict, keys_to_remove) -> dict:
        return {
            key: self.__remove_null_values(value, keys_to_remove) if isinstance(value, dict) else value
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
    def __create_arguments(self, id_first_entity: str, sort_key=None) -> dict:
        sort_key = self._single_entity_storage_keyword if sort_key is None else sort_key
        return {
            self.get_partition_key_table(): id_first_entity,
            self.get_sort_key_table(): sort_key
        }
    """


def __generate_update_expression() -> str:
    """
    This function generates the code for the update_expression function.
    :return: The code for the update_expression function.
    """
    return """
    @staticmethod
    def create_update_expression(arguments):
        return 'SET ' + ', '.join([f'{key} = :{key}' for key in arguments.keys()])
    """


def __generate_create_expression_attribute_values() -> str:
    """
    This function generates the code for the create_expression_attribute_values function.
    :return: The code for the create_expression_attribute_values function.
    """
    return """
    @staticmethod
    def create_expression_attribute_values(arguments):
        return {f':{key}': value for key, value in arguments.items()}
    """