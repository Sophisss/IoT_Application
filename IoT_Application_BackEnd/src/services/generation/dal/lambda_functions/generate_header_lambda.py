def generate_header_lambda(name, table_name, tables):
    def generate_dynamo_instance():
        table_found = next(filter(lambda table: table_name == table['tableName'], tables), None)
        return f"""dynamodb_manager = DynamoManager(Configuration('{table_found['tableName']}','{table_found['parameters']['id_separator']}',
                                                '{table_found['partition_key']['name']}','{table_found['sort_key']['name']}',
                                                '{table_found['parameters']['single_entity_storage_keyword']}','{table_found['GSI']['index_name']}'))"""

    return f"""from configuration import Configuration 
from dynamo_class import DynamoManager 
from event.event import Event 
from event.event_parse import parse_event 
from exception_class import IdAlreadyExistsError, ItemNotPresentError, EntitiesNotPresentError
from model.{name.lower()} import {name}

{generate_dynamo_instance()}
"""
