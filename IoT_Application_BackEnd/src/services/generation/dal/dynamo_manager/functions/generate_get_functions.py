def generate_get_functions() -> str:
    """
    This function generates the code for the get functions.
    :return: The code for the get functions.
    """
    return f"""{__generate_get_item()}
{__generate_get_items()}
{__generate_get_items_with_secondary_index()}
{__generate_get_pk()}
{__generate_get_sk()}
{__generate_get_attr()}
    """


def __generate_get_item() -> str:
    """
    This function generates the code for the get_item function.
    :return: The code for the get_item function.
    """
    return """    def get_item(self, partition_key: str, sort_key=None) -> Optional[dict]:
        response = self.configuration.table.get_item(
            Key=self.__create_arguments(partition_key, sort_key))
        return response['Item'] if 'Item' in response else None
    """


def __generate_get_items() -> str:
    """
    This function generates the code for the get_items function.
    :return: The code for the get_items function.
    """
    return """    def get_items(self, partition_key, prefix=None) -> Optional[list[dict]]:
        key_condition_expression = Key(self.get_partition_key_table()).eq(partition_key) if prefix is None else Key(
            self.get_partition_key_table()).eq(partition_key) & Key(self.get_sort_key_table()).begins_with(prefix)
        response = self.configuration.table.query(KeyConditionExpression=key_condition_expression)
        print(response['Items'])
        return response['Items'] if response['Items'] else None
    """


def __generate_get_items_with_secondary_index() -> str:
    """
    This function generates the code for the get_items_with_secondary_index function.
    :return: The code for the get_items_with_secondary_index function.
    """
    return """    def get_items_with_secondary_index(self, prefix=None, key=None) -> Optional[list[dict]]:
        key = self.configuration.single_entity_storage_keyword if key is None else key
        key_condition_expression = Key(self.get_sort_key_table()).eq(key) if prefix is None else Key(
            self.get_sort_key_table()).eq(key) & Key(self.get_partition_key_table()).begins_with(prefix)
        response = self.configuration.table.query(
            IndexName=self.configuration.gsi,
            KeyConditionExpression=key_condition_expression)
        return response['Items'] if response['Items'] else None
    """


def __generate_get_pk() -> str:
    """
    This function generates the code for the get_partition_key_table function.
    :return: The code for the get_partition_key_table function.
    """
    return """    def get_partition_key_table(self) -> str:
        return self.configuration.partition_key_table
    """


def __generate_get_sk() -> str:
    """
    This function generates the code for the get_sort_key_table function.
    :return: The code for the get_sort_key_table function.
    """
    return """    def get_sort_key_table(self) -> str:
        return self.configuration.sort_key_table
    """


def __generate_get_attr() -> str:
    """
    This function generates the code for the get_attr function.
    :return: The code for the get_attr function.
    """
    return """    @staticmethod
    def __getAttr(object_to_get_attr, id_key: str):
        return getattr(object_to_get_attr, id_key)"""
