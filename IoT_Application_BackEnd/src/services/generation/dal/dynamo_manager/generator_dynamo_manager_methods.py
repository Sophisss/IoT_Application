def generate_methods() -> str:
    """
    This function generates the code for the methods of the DynamoDBManager class.
    :return: The code for the methods of the DynamoDBManager class.
    """
    return f"""{__generate_put_item_method()}
{__generate_delete_item_method()}
{__generate_remove_associated_link_method()}
{__generate_delete_method()}
{__generate_update_item_method()}
{__generate_get_items_method()}
{__generate_get_item_method()}
{__generate_get_items_with_secondary_index_method()}
{__generate_create_update_expression_method()}
{__generate_create_expression_attribute_values_method()}
"""


def __generate_put_item_method() -> str:
    """
    This function generates the function used to put an item in the database.
    :return: The function used to put an item in the database.
    """
    return """    def put_item(self, table_name: str, item: dict) -> dict:
        table = self.dynamodb.Table(table_name)
        return table.put_item(Item=item)
    """


def __generate_delete_item_method() -> str:
    """
    This function generates the function used to delete an item from the database.
    :return: The function used to delete an item from the database.
    """
    return """    def delete_item(self, table_name: str, item_keys: dict):
        table = self.dynamodb.Table(table_name)
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

        sort_key = list(item_keys.keys())[1]

        if response is not None:
            for item in response:
                if item[sort_key] != item_keys[sort_key]:
                    self.__delete(table, item)

        partition_key = list(item_keys.keys())[1]

        response = table.query(
            IndexName=index_name,
            KeyConditionExpression=Key(sort_key).eq(item_keys[partition_key])
        )

        if response['Items'] is not None:
            for item in response['Items']:
                if item[partition_key] != item_keys[sort_key]:
                    self.__delete(table, item)
    """


def __generate_delete_method() -> str:
    """
    This function generates the function used to delete an item from the database.
    :return: The function used to delete an item from the database.
    """
    return """    @staticmethod
    def __delete(table, key: dict):
        return table.delete_item(
            Key=key,
            ReturnValues='ALL_OLD'
        )
    """


def __generate_update_item_method() -> str:
    """
    This function generates the function used to update an item in the database.
    :return: The function used to update an item in the database.
    """
    return """    def update_item(self, table_name: str, item_keys: dict, arguments: dict):
        table = self.dynamodb.Table(table_name)
        return table.update_item(
            Key=item_keys,
            UpdateExpression=self.__create_update_expression(arguments),
            ExpressionAttributeValues=self.__create_expression_attribute_values(arguments),
            ReturnValues='ALL_NEW'
        )
    """


def __generate_get_items_method() -> str:
    """
    This function generates the function used to get items from the database.
    :return: The function used to get items from the database.
    """
    return """    def get_items(self, table_name: str, item_keys: dict):
        table = self.dynamodb.Table(table_name)

        partition_key = list(item_keys.keys())[0]
        key_condition_expression = Key(partition_key).eq(item_keys[partition_key])
        response = table.query(KeyConditionExpression=key_condition_expression)

        return response['Items'] if response['Items'] else None
    """


def __generate_get_item_method() -> str:
    """
    This function generates the function used to get an item from the database.
    :return: The function used to get an item from the database.
    """
    return """    def get_item(self, table_name: str, key: dict):
        table = self.dynamodb.Table(table_name)
        response = table.get_item(Key=key)
        return response['Item'] if 'Item' in response else None
    """


def __generate_get_items_with_secondary_index_method() -> str:
    """
    This function generates the function used to get items with a secondary index from the database.
    :return: The function used to get items with a secondary index from the database.
    """
    return """    def get_items_with_secondary_index(self, table_name: str, index_name: str, item_keys: dict):
        table = self.dynamodb.Table(table_name)

        partition_key = list(item_keys.keys())[0]
        sort_key = list(item_keys.keys())[1]

        key_condition_expression = Key(partition_key).eq(item_keys[partition_key]) & Key(sort_key).begins_with(
            item_keys[sort_key])

        response = table.query(
            IndexName=index_name,
            KeyConditionExpression=key_condition_expression)

        return response['Items'] if response['Items'] else None
    """


def __generate_create_update_expression_method() -> str:
    """
    This function generates the function used to create the update expression for an item.
    :return: The function used to create the update expression for an item.
    """
    return """    @staticmethod
    def __create_update_expression(arguments: dict) -> str:
        return 'SET ' + ', '.join([f'{key} = :{key}' for key in arguments.keys()])
    """


def __generate_create_expression_attribute_values_method() -> str:
    """
    This function generates the function used to create the expression attribute values for an item.
    :return: The function used to create the expression attribute values for an item.
    """
    return """    @staticmethod
    def __create_expression_attribute_values(arguments: dict) -> dict:
        return {f':{key}': value for key, value in arguments.items()}
    """
