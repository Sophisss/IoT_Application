def generate_configuration_methods() -> str:
    """
    This function generates the methods of the configuration class.
    :return: The methods of the configuration class.
    """
    return f"""
{__generate_instance_table_method()}
{__generate_get_table_method()}
{__generate_get_separator_method()}
{__generate_get_pk_method()}
{__generate_get_sk_method()}
{__generate_get_storage_keyword_method()}
{__generate_gsi_method()}
    """


def __generate_instance_table_method() -> str:
    """
    This function generates the code for the instance_table method.
    :return: The code for the instance_table method.
    """
    return """    def __instance_table(self, table_name: str):
        self._dynamodb = boto3.resource('dynamodb')
        return self._dynamodb.Table(table_name)
        """


def __generate_get_table_method() -> str:
    """
    This function generates the code for the get_table method.
    :return: The code for the get_table method.
    """
    return """    def get_table(self):
        return self.table
        """


def __generate_get_separator_method() -> str:
    """
    This function generates the code for the get_separator method.
    :return: The code for the get_separator method.
    """
    return """    def get_separator(self) -> str:
        return self.separator
        """


def __generate_get_pk_method() -> str:
    """
    This function generates the code for the get_partition_key_table method.
    :return: The code for the get_partition_key_table method.
    """
    return """    def get_pk_table(self) -> str:
        return self.partition_key_table
        """


def __generate_get_sk_method() -> str:
    """
    This function generates the code for the get_sort_key_table method.
    :return: The code for the get_sort_key_table method.
    """
    return """    def get_sk_table(self) -> str:
        return self.sort_key_table
        """


def __generate_get_storage_keyword_method() -> str:
    """
    This function generates the code for the get_storage_keyword method.
    :return: The code for the get_storage_keyword method.
    """
    return """    def get_storage_keyword(self) -> str:
        return self.single_entity_storage_keyword
        """


def __generate_gsi_method() -> str:
    return """    def get_global_secondary_index(self) -> str:
        return self.gsi"""
