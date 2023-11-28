def generate_header(name: str, table_name: str, tables: dict) -> str:
    """
    This function generates the lambda header.
    :param name: the name of the item.
    :param table_name: the table name of the item.
    :param tables: dict of existing tables.
    :return: the code of the lambda header.
    """
    return f"""from configuration import Configuration 
from dynamo_class import DynamoManager 
from event.event import Event 
from event.event_parse import parse_event 
from exception_class import IdAlreadyExistsError, ItemNotPresentError, EntitiesNotPresentError
from model.{name.lower()} import {name}

{__generate_dynamo_instance(table_name, tables)}
"""


def __generate_dynamo_instance(table_name: str, tables: dict) -> str:
    """
    This function generates the dynamo instance.
    :param table_name: the table name.
    :param tables: dict of existing tables.
    :return: the code of the dynamo instance.
    """
    table_found = next(filter(lambda table: table_name == table['tableName'], tables), None)
    return f"""dynamodb_manager = DynamoManager(Configuration('{table_found['tableName']}','{table_found['parameters']['id_separator']}',
                                                '{table_found['partition_key']['name']}','{table_found['sort_key']['name']}',
                                                '{table_found['parameters']['single_entity_storage_keyword']}','{table_found['GSI']['index_name']}'))
    """
