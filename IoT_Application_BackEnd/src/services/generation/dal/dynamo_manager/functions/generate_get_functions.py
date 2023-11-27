def generate_get_functions() -> str:
    """
    This function generates the code for the get functions.
    :return: The code for the get functions.
    """
    return f"""{__generate_get_item()}
{__generate_get_items()}
{__generate_get_items_with_secondary_index()}
{__generate_get_configuration_method()}
    """


def __generate_get_item() -> str:
    """
    This function generates the code for the get_item function.
    :return: The code for the get_item function.
    """
    return """    def get_item(self, partition_key, sort_key: Optional = None) -> Optional[dict]:
        response = self.get_configuration().get_table().get_item(
            Key=create_arguments(self.get_configuration().get_storage_keyword(),
                                 self.get_configuration().get_pk_table(),
                                 self.get_configuration().get_sk_table(), partition_key, sort_key))
        return response['Item'] if 'Item' in response else None
    """


def __generate_get_items() -> str:
    """
    This function generates the code for the get_items function.
    :return: The code for the get_items function.
    """
    return """    def get_items(self, partition_key, prefix: Optional[str] = None) -> Optional[list[dict]]:
        key_condition_expression = Key(self.get_configuration().get_pk_table()).eq(
            partition_key) if prefix is None else Key(
            self.get_configuration().get_pk_table()).eq(partition_key) & Key(
            self.get_configuration().get_sk_table()).begins_with(prefix)

        response = self.get_configuration().get_table().query(KeyConditionExpression=key_condition_expression)
        return response['Items'] if response['Items'] else None
    """


def __generate_get_items_with_secondary_index() -> str:
    """
    This function generates the code for the get_items_with_secondary_index function.
    :return: The code for the get_items_with_secondary_index function.
    """
    return """    def get_items_with_secondary_index(self, prefix=None, key=None) -> Optional[list[dict]]:
        key = self.get_configuration().get_storage_keyword() if key is None else key
        key_condition_expression = Key(self.get_configuration().get_sk_table()).eq(
            key) if prefix is None else Key(
            self.get_configuration().get_sk_table()).eq(key) & Key(
            self.get_configuration().get_pk_table()).begins_with(prefix)

        response = self.get_configuration().get_table().query(
            IndexName=self.get_configuration().get_global_secondary_index(),
            KeyConditionExpression=key_condition_expression)
        return response['Items'] if response['Items'] else None
        """


def __generate_get_configuration_method() -> str:
    """
    This function generates the code for the get_configuration method.
    :return: The code for the get_configuration method.
    """
    return """    def get_configuration(self) -> Configuration:
        return self.configuration
    """
