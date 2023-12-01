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
        self.__validate_table_name(table_name)
        if not item or not isinstance(item, dict):
            raise Exception("item is mandatory and it must be a dictionary")
        if self.get_item(table_name, item) is not None:
            raise IdAlreadyExistsError()

        response = self.dynamodb.Table(table_name).put_item(Item=self.__remove_null_values(item))
        BaseAWSService.validate_aws_response(self, response, "put_item")
        return response
    """


def __generate_delete_item_method() -> str:
    """
    This function generates the function used to delete an item from the database.
    :return: The function used to delete an item from the database.
    """
    return """    def delete_item(self, table_name: str, item_keys: dict) -> dict:
        self.__validate_table_name(table_name)
        self.__validate_record_key(item_keys)
        check_response_item(self.get_item(table_name, item_keys))

        response = self.__delete(self.dynamodb.Table(table_name), item_keys)
        BaseAWSService.validate_aws_response(self, response, "delete_item")
        return response
    """


def __generate_remove_associated_link_method() -> str:
    """
    This function generates the function used to remove an associated link from the database.
    :return: The function used to remove an associated link from the database.
    """
    return """    def remove_associated_link(self, table_name: str, index_name: str, item_keys: dict):
        self.__validate_table_name(table_name)
        self.__validate_record_key(item_keys)
        if not index_name or not isinstance(index_name, str):
            raise Exception("index_name is mandatory and it must be a string")

        table = self.dynamodb.Table(table_name)
        partition_key, sort_key = self.get_partition_sort_key(item_keys)

        response = self.get_items(table_name, Key(partition_key).eq(item_keys[partition_key]))
        check_response_item(response)
        self.remove_link(response, item_keys, table, partition_key=sort_key, sort_key=sort_key)

        response = self.get_items(table_name, Key(sort_key).eq(item_keys[partition_key]), index=index_name)
        check_response_item(response)
        self.remove_link(response, item_keys, table, partition_key=partition_key, sort_key=sort_key)
    """


def __generate_update_item_method() -> str:
    """
    This function generates the function used to update an item in the database.
    :return: The function used to update an item in the database.
    """
    return """    def update_item(self, table_name: str, item_keys: dict, arguments: dict) -> dict:
        self.__validate_table_name(table_name)
        self.__validate_record_key(item_keys)
        check_response_item(self.get_item(table_name, item_keys))

        response = self.dynamodb.Table(table_name).update_item(
            Key=item_keys,
            UpdateExpression=self.__create_update_expression(arguments),
            ExpressionAttributeValues=self.__create_expression_attribute_values(arguments),
            ReturnValues='UPDATED_NEW'
        )
        BaseAWSService.validate_aws_response(self, response, "update_item")
        return response
    """


def __generate_get_methods() -> str:
    """
    This function generates the functions used to get items from the database.
    :return: The functions used to get items from the database.
    """
    return f"""{__generate_get_item_method()}
{__generate_get_items_method()}
    """


def __generate_get_item_method() -> str:
    """
    This function generates the function used to get an item from the database.
    :return: The function used to get an item from the database.
    """
    return """    def get_item(self, table_name: str, key: dict):
        self.__validate_table_name(table_name)
        self.__validate_record_key(key)
        response = self.dynamodb.Table(table_name).get_item(Key=key)
        return response if response.get(self.ITEM) else None
    """


def __generate_get_items_method() -> str:
    """
    This function generates the function used to get items from the database.
    :return: The function used to get items from the database.
    """
    return """    def get_items(self, table_name: str, query, index=None):
        self.__validate_table_name(table_name)
        if not query:
            raise Exception("query is mandatory")
        if index is not None and not isinstance(index, str):
            raise Exception("index must be a string")

        if index:
            response = self.dynamodb.Table(table_name).query(KeyConditionExpression=query, IndexName=index)
        else:
            response = self.dynamodb.Table(table_name).query(KeyConditionExpression=query)

        return response if response.get(self.ITEMS) else None
    """


def __generate_remove_link_method() -> str:
    """
    This function generates the function used to remove a link from the database.
    :return: The function used to remove a link from the database.
    """
    return """    def remove_link(self, response: Optional, item_keys: dict, table, partition_key: str, sort_key: str):
        if response is not None:
            for item in response['Items']:
                if item[partition_key] != f'{item_keys[sort_key]}':
                    check_response_status(self.__delete(table, item))
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
    return f"""{__generate_validate_record_key_method()}
{__generate_validate_table_name_method()}
{__generate_delete_method()}
{__generate_get_partition_sort_key_method()}
{__generate_create_update_expression_method()}
{__generate_create_expression_attribute_values_method()}
    """


def __generate_validate_record_key_method() -> str:
    """
    This function generates the function used to validate a record key.
    :return: The function used to validate a record key.
    """
    return """    @staticmethod
    def __validate_record_key(key: dict):
        if not key or not isinstance(key, dict):
            raise Exception("key is mandatory and it must be a dictionary")
    """


def __generate_validate_table_name_method() -> str:
    """
    This function generates the function used to validate a table name.
    :return: The function used to validate a table name.
    """
    return """    @staticmethod
    def __validate_table_name(table_name: str):
        if not table_name or not isinstance(table_name, str):
            raise Exception("table_name is mandatory and it must be a string")
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
