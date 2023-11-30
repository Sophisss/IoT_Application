def generate_methods() -> str:
    """
    This function generates the code for the methods of the DynamoDBManager class.
    :return: The code for the methods of the DynamoDBManager class.
    """
    return f"""{__generate_put_item_method()}
{__generate_delete_item_method()}
{__generate_remove_associated_link_method()}
{__generate_update_item_method()}
{__generate_get_methods()}
{__generate_remove_null_values_method()}
{__generate_static_methods()}"""


def __generate_put_item_method() -> str:
    """
    This function generates the function used to put an item in the database.
    :return: The function used to put an item in the database.
    """
    return """    def put_item(self, table_name: str, item: dict) -> dict:
        table = self.dynamodb.Table(table_name)
        if self.get_item(table_name, item) is not None:
            raise IdAlreadyExistsError()
        return table.put_item(Item=self.__remove_null_values(item))
    """


def __generate_delete_item_method() -> str:
    """
    This function generates the function used to delete an item from the database.
    :return: The function used to delete an item from the database.
    """
    return """    def delete_item(self, table_name: str, item_keys: dict) -> dict:
        table = self.dynamodb.Table(table_name)
        check_response_item(self.get_item(table_name, item_keys))
        return self.__delete(table, item_keys)
    """


def __generate_remove_associated_link_method() -> str:
    """
    This function generates the function used to remove an associated link from the database.
    :return: The function used to remove an associated link from the database.
    """
    return """    def remove_associated_link(self, table_name: str, index_name: str, item_keys: dict):
        table = self.dynamodb.Table(table_name)
        response = self.get_items(table_name, item_keys)
        check_response_item(response)

        partition_key, sort_key = self.get_partition_sort_key(item_keys)

        if response is not None:
            for item in response['Items']:
                if item[sort_key] != f'{item_keys[sort_key]}':
                    check_response_status(self.__delete(table, item))

        response = self.get_items_gsi(table_name, index_name, item_keys)
        check_response_item(response)

        if response is not None:
            for item in response['Items']:
                if item[partition_key] != f'{item_keys[sort_key]}':
                    check_response_status(self.__delete(table, item))
    """


def __generate_update_item_method() -> str:
    """
    This function generates the function used to update an item in the database.
    :return: The function used to update an item in the database.
    """
    return """    def update_item(self, table_name: str, item_keys: dict, arguments: dict) -> dict:
        table = self.dynamodb.Table(table_name)
        check_response_item(self.get_item(table_name, item_keys))
        return table.update_item(
            Key=item_keys,
            UpdateExpression=self.__create_update_expression(arguments),
            ExpressionAttributeValues=self.__create_expression_attribute_values(arguments),
            ReturnValues='ALL_NEW'
        )
    """


def __generate_get_methods() -> str:
    """
    This function generates the functions used to get items from the database.
    :return: The functions used to get items from the database.
    """
    return f"""{__generate_get_items_method()}
{__generate_get_items_gsi_method()}
{__generate_get_item_method()}
{__generate_get_items_with_secondary_index_method()}
    """


def __generate_get_items_method() -> str:
    """
    This function generates the function used to get items from the database.
    :return: The function used to get items from the database.
    """
    return """    def get_items(self, table_name: str, item_keys: dict) -> Optional[dict]:
        table = self.dynamodb.Table(table_name)

        partition_key = self.get_partition_sort_key(item_keys)[0]
        key_condition_expression = Key(partition_key).eq(item_keys[partition_key])
        response = self.__query_table(table, key_condition_expression)

        return response if response['Items'] else None
    """


def __generate_get_items_gsi_method() -> str:
    """
    This function generates the function used to get items with a global secondary index from the database.
    :return: The function used to get items with a global secondary index from the database.
    """
    return """    def get_items_gsi(self, table_name: str, index_name: str, item_keys: dict) -> Optional[dict]:
        table = self.dynamodb.Table(table_name)
        partition_key, sort_key = self.get_partition_sort_key(item_keys)

        key_condition_expression = Key(sort_key).eq(item_keys[partition_key])
        response = self.__query_table(table, key_condition_expression, index_name)
        return response if response['Items'] else None
    """


def __generate_get_item_method() -> str:
    """
    This function generates the function used to get an item from the database.
    :return: The function used to get an item from the database.
    """
    return """    def get_item(self, table_name: str, key: dict) -> Optional[dict]:
        table = self.dynamodb.Table(table_name)
        response = table.get_item(Key=key)
        return response if 'Item' in response else None
    """


def __generate_get_items_with_secondary_index_method() -> str:
    """
    This function generates the function used to get items with a secondary index from the database.
    :return: The function used to get items with a secondary index from the database.
    """
    return """    def get_items_with_secondary_index(self, table_name: str, index_name: str, item_keys: dict) -> Optional[dict]:
        table = self.dynamodb.Table(table_name)
        partition_key, sort_key = self.get_partition_sort_key(item_keys)

        key_condition_expression = Key(partition_key).eq(item_keys[partition_key]) & Key(sort_key).begins_with(
            item_keys[sort_key])

        response = self.__query_table(table, key_condition_expression, index_name)
        return response if response['Items'] else None
    """


def __generate_remove_null_values_method() -> str:
    """
    This function generates the function used to remove null values from a dictionary.
    :return: The function used to remove null values from a dictionary.
    """
    return """    def __remove_null_values(self, dictionary: dict) -> dict:
        return {
            key: self.__remove_null_values(value) if isinstance(value, dict) else value
            for key, value in dictionary.items()
            if value is not None
        }
    """


def __generate_static_methods() -> str:
    """
    This function generates the static methods of the DynamoDBManager class.
    :return: The static methods of the DynamoDBManager class.
    """
    return f"""{__generate_query_table_method()}
{__generate_delete_method()}
{__generate_get_partition_sort_key_method()}
{__generate_create_update_expression_method()}
{__generate_create_expression_attribute_values_method()}
    """


def __generate_query_table_method() -> str:
    """
    This function generates the function used to query a table.
    :return: The function used to query a table.
    """
    return """    @staticmethod
    def __query_table(table, key_conditions, index_name: Optional[str] = None) -> dict:
        if index_name:
            return table.query(IndexName=index_name, KeyConditionExpression=key_conditions)
        else:
            return table.query(KeyConditionExpression=key_conditions)
    """


def __generate_delete_method() -> str:
    """
    This function generates the function used to delete an item from the database.
    :return: The function used to delete an item from the database.
    """
    return """    @staticmethod
    def __delete(table, key: dict) -> dict:
        return table.delete_item(
            Key=key,
            ReturnValues='ALL_OLD'
        )
    """


def __generate_get_partition_sort_key_method() -> str:
    """
    This function generates the function used to get the partition and sort keys from a dictionary.
    :return: The function used to get the partition and sort keys from a dictionary.
    """
    return """    @staticmethod
    def get_partition_sort_key(item_keys: dict) -> tuple:
        partition_key = list(item_keys.keys())[0]
        sort_key = list(item_keys.keys())[1]
        return partition_key, sort_key
    """


def __generate_create_update_expression_method() -> str:
    """
    This function generates the function used to create the update expression for an item.
    :return: The function used to create the update expression for an item.
    """
    return """    @staticmethod
    def __create_update_expression(arguments: dict) -> str:
        return f"SET {', '.join([f'{key} = :{key}' for key in arguments.keys()])}"
    """


def __generate_create_expression_attribute_values_method() -> str:
    """
    This function generates the function used to create the expression attribute values for an item.
    :return: The function used to create the expression attribute values for an item.
    """
    return """    @staticmethod
    def __create_expression_attribute_values(arguments: dict) -> dict:
        return {f':{key}': value for key, value in arguments.items()}"""
