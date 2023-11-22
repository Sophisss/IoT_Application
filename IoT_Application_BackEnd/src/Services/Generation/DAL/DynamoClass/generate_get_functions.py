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
    """


def __generate_get_item() -> str:
    """
    This function generates the code for the get_item function.
    :return: The code for the get_item function.
    """
    return """
    def get_item(self, partition_key: str, sort_key=None) -> Optional[dict]:
        response = self._table.get_item(
            Key=self.__create_arguments(partition_key, sort_key))
        return response['Item'] if 'Item' in response else None
    """


def __generate_get_items() -> str:
    """
    This function generates the code for the get_items function.
    :return: The code for the get_items function.
    """
    return """
    def get_items(self, partition_key, prefix):
        response = self._table.query(
            KeyConditionExpression=(
                    Key(self.get_partition_key_table()).eq(partition_key) & Key(self.get_sort_key_table()).begins_with(prefix)
            )
        )
        return response['Items']
    """


def __generate_get_items_with_secondary_index() -> str:
    """
    This function generates the code for the get_items_with_secondary_index function.
    :return: The code for the get_items_with_secondary_index function.
    """
    return """
    def get_items_with_secondary_index(self, prefix, key=None) -> Optional[list[dict]]:
        key = self._single_entity_storage_keyword if key is None else key
        response = self._table.query(
            IndexName=self._GSI,
            KeyConditionExpression=(
                    Key(self.get_sort_key_table()).eq(key) & Key(self.get_partition_key_table()).begins_with(prefix)
            )
        )
        return response['Items'] if response['Items'] is not None else None
    """


def __generate_get_pk() -> str:
    """
    This function generates the code for the get_partition_key_table function.
    :return: The code for the get_partition_key_table function.
    """
    return """
    def get_partition_key_table(self) -> str:
        return self._partition_key_table
    """


def __generate_get_sk() -> str:
    """
    This function generates the code for the get_sort_key_table function.
    :return: The code for the get_sort_key_table function.
    """
    return """
    def get_sort_key_table(self) -> str:
        return self._sort_key_table
    """
