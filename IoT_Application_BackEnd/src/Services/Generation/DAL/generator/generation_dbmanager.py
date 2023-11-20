def generator_dbmanager():
    return f"""
import boto3
from boto3.dynamodb.conditions import Key
from ExceptionClasses import IdAlreadyExistsError


class DynamoDBManager:
    def __init__(self, table_name, separator, partition_key_table, sort_key_table, single_entity_storage_keyword, gsi):
        self._dynamodb = boto3.resource('dynamodb')
        self._table = self._dynamodb.Table(table_name)
        self._separator = separator
        self._partition_key_table = partition_key_table
        self._sort_key_table = sort_key_table
        self._single_entity_storage_keyword = single_entity_storage_keyword
        self._GSI = gsi

    def create_entity(self, name_entity, name_id, event_arguments):
        id_entity = f"{{name_entity}}{{self._separator}}{{event_arguments.pop(name_id)}}"
        if self.get_item(id_entity):
            raise IdAlreadyExistsError(name_entity, id_entity)
        arguments = {{
            self._partition_key_table: id_entity,
            self._sort_key_table: self._single_entity_storage_keyword
        }}
        event_arguments.update(arguments)
        return self._table.put_item(Item=event_arguments)

    def create_link(self, first_entity_id, second_entity_id, event_arguments):
        event_arguments[self._partition_key_table] = first_entity_id
        event_arguments[self._sort_key_table] = second_entity_id
        return self._table.put_item(Item=event_arguments)

    def delete_item(self, partition_key, sort_key=None):
        if sort_key is None:
            sort_key = self._single_entity_storage_keyword
        response = self._table.delete_item(
            Key={{
                self._partition_key_table: partition_key,
                self._sort_key_table: sort_key
            }},
            ReturnValues='ALL_OLD'
        )
        if 'Attributes' in response:
            return response['Attributes']
        else:
            return None

    def get_item(self, partition_key, sort_key=None):
        if sort_key is None:
            sort_key = self._single_entity_storage_keyword
        response = self._table.get_item(
            Key={{
                self._partition_key_table: partition_key,
                self._sort_key_table: sort_key
            }}
        )
        if 'Item' in response:
            return response['Item']
        else:
            return None

    def get_items(self, partition_key, prefix):
        response = self._table.query(
            KeyConditionExpression=(
                    Key(self._partition_key_table).eq(partition_key) & Key(self._sort_key_table).begins_with(prefix)
            )
        )
        return response['Items']

    def get_items_with_secondary_index(self, prefix, key=None):
        if key is None:
            key = self._single_entity_storage_keyword
        response = self._table.query(
            IndexName=self._GSI,
            KeyConditionExpression=(
                    Key(self._sort_key_table).eq(key) & Key(self._partition_key_table).begins_with(prefix)
            )
        )
        if response['Items'] is None:
            return None
        return response['Items']

    def create_id_entity(self, name_entity, name_id, event_arguments):
        id_entity = f"{{name_entity}}{{self._separator}}{{event_arguments.pop(name_id)}}"
        return id_entity

    def get_partition_key_table(self):
        return self._partition_key_table

    def get_sort_key_table(self):
        return self._sort_key_table
"""
