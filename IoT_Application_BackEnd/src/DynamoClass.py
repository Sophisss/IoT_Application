import boto3
from typing import Optional
from ExceptionClasses import IdAlreadyExistsError
from Link import BuildingDevice
from MODEL import Device
from boto3.dynamodb.conditions import Key


class DynamoDBManager:
    """
    This class represents a DynamoDBManager.
    It is responsible for all the operations that are related to DynamoDB.
    """

    def __init__(self, table_name, separator, partition_key_table, sort_key_table, single_entity_storage_keyword, gsi):
        self._dynamodb = boto3.resource('dynamodb')
        self._table = self._dynamodb.Table(table_name)
        self._separator = separator
        self._partition_key_table = partition_key_table
        self._sort_key_table = sort_key_table
        self._single_entity_storage_keyword = single_entity_storage_keyword
        self._GSI = gsi

    def create_device(self, arguments: dict) -> tuple:
        """
        This method creates a device model and puts it in the DynamoDB table.
        :param arguments: The arguments that are needed to create a device.
        :return: The response of the put_item method and the id of the device.
        """
        device = Device(**arguments)
        return self.__put_entity("Device", device.device_id, device), device.device_id

    def create_building(self, arguments: dict) -> tuple:
        pass

    def __put_entity(self, name: str, entity_id, entity) -> dict:
        """
        This method puts an entity in the DynamoDB table.
        :param name: The name of the entity.
        :param entity: The entity that needs to be put in the DynamoDB table.
        :return: The response of the put_item method.
        """
        id_entity = self.create_id(name, entity_id)
        if self.get_item(id_entity):
            raise IdAlreadyExistsError(name, id_entity)

        event_arguments = self.remove_null_values(entity.model_dump(), [f'{name}_id'.lower()])
        event_arguments.update(self.create_arguments(id_entity))

        return self._table.put_item(Item=event_arguments)

    def create_link_building_device(self, arguments: dict) -> dict:
        """
        This method creates a link between a device and a building.
        :param arguments: The arguments that are needed to create a link between a device and a building.
        :return: The response of the put_item method.
        """
        link = BuildingDevice(**arguments)
        return self.__put_link(link, "Building", "Device", link.building_id, link.device_id)

    def __put_link(self, link, name_first_entity: str, name_second_entity: str, first_entity_id,
                   second_entity_id) -> dict:
        """
        This method puts a link between two entities in the DynamoDB table.
        :param link: The link that needs to be put in the DynamoDB table.
        :param name_first_entity: The name of the first entity.
        :param name_second_entity: The name of the second entity.
        :return: The response of the put_item method.
        """
        id_first_entity = self.create_id(name_first_entity, first_entity_id)
        id_second_entity = self.create_id(name_second_entity, second_entity_id)

        event_arguments = self.remove_null_values(link.model_dump(), [f'{name_first_entity}_id'.lower(),
                                                                      f'{name_second_entity}_id'.lower()])
        event_arguments.update(self.create_arguments(id_first_entity, id_second_entity))

        return self._table.put_item(Item=event_arguments)

    def delete_device(self, device_id: str) -> tuple[Optional[dict], str]:
        """
        This method deletes a device from the DynamoDB table.
        :param device_id: The id of the device that needs to be deleted.
        :return: The response of the delete_item method.
        """
        return self.__delete_item("Device", device_id), device_id

    def delete_building(self, building_id: str) -> tuple[Optional[dict], str]:
        pass

    def delete_link_building_device(self, building_id: str, device_id: str) -> tuple[Optional[dict], str, str]:
        pass

    def __delete_item(self, name, partition_key: str, sort_key=None) -> Optional[dict]:
        """
        This method deletes an item from the DynamoDB table.
        :param partition_key: The partition key of the item.
        :param sort_key: The sort key of the item.
        :return: The response of the delete_item method if the item was deleted, None otherwise.
        """
        sort_key = self.create_id(name, sort_key) if sort_key is not None else self._single_entity_storage_keyword
        response = self._table.delete_item(
            Key={
                self._partition_key_table: self.create_id(name, partition_key),
                self._sort_key_table: sort_key
            },
            ReturnValues='ALL_OLD'
        )
        if 'Attributes' in response:
            return response['Attributes']
        else:
            return None

    # utility functions

    def get_item(self, partition_key: str, sort_key=None) -> Optional[dict]:
        """
        This method gets an item from the DynamoDB table.
        :param partition_key: The partition key of the item.
        :param sort_key: The sort key of the item.
        :return: The item that was requested.
        """
        sort_key = self._single_entity_storage_keyword if sort_key is None else sort_key
        response = self._table.get_item(
            Key={
                self._partition_key_table: partition_key,
                self._sort_key_table: sort_key
            }
        )
        if 'Item' in response:
            return response['Item']
        else:
            return None

    def create_id(self, name: str, object_id: str) -> str:
        """
        This method creates an id for an object.
        :param name: The name of the object.
        :param object_id: The id of the object.
        :return: The id of the object.
        """
        return f"{name}{self._separator}{object_id}"

    def remove_null_values(self, dictionary: dict, keys_to_remove) -> dict:
        """
        This method removes all the null values from a dictionary.
        :param dictionary: The dictionary that needs to be cleaned.
        :param keys_to_remove: The keys that need to be removed.
        :return: The cleaned dictionary.
        """
        return {
            key: self.remove_null_values(value, keys_to_remove) if isinstance(value, dict) else value
            for key, value in dictionary.items()
            if value is not None and key not in keys_to_remove
        }

    def create_arguments(self, id_first_entity: str, sort_key=None) -> dict:
        """
        This method creates the arguments that are needed to put an item in the DynamoDB table.
        :param id_first_entity: The id of the first entity.
        :param sort_key: The sort key of the item.
        :return: The arguments that are needed to put an item in the DynamoDB table.
        """
        sort_key = self._single_entity_storage_keyword if sort_key is None else sort_key
        return {
            self._partition_key_table: id_first_entity,
            self._sort_key_table: sort_key
        }

    def get_partition_key_table(self) -> str:
        """
        This method returns the name of the partition key table.
        :return: The name of the partition key table.
        """
        return self._partition_key_table

    def get_sort_key_table(self) -> str:
        """
        This method returns the name of the sort key table.
        :return: The name of the sort key table.
        """
        return self._sort_key_table

    def get_items_with_secondary_index(self, prefix, key=None) -> Optional[list[dict]]:
        """
        This method gets all the items with a secondary index.
        :param prefix: The prefix of the items.
        :param key: The key of the items.
        :return: The items that were requested if they exist, None otherwise.
        """
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

    def get_items(self, partition_key, prefix):
        """
        This method gets all the items with a secondary index.
        :param partition_key: The partition key of the items.
        :param prefix: The prefix of the items.
        :return: The items that were requested.
        """
        response = self._table.query(
            KeyConditionExpression=(
                    Key(self._partition_key_table).eq(partition_key) & Key(self._sort_key_table).begins_with(prefix)
            )
        )
        return response['Items']
