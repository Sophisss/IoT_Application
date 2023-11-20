def generator_header_api(json):
    table = json['awsConfig']['dynamo']['tables'][0]
    parameters = json['parameters']
    return f"""
from DynamoClass import DynamoDBManager
from ExceptionClasses import IdAlreadyExistsError, ItemNotPresentError, EntitiesNotPresentError

dynamodb_manager = DynamoDBManager('{table['tableName']}', '{parameters['id_separator']}', '{table['partition_key']['name']}', '{table['sort_key']['name']}',
                                   '{parameters['single_entity_storage_keyword']}', '{table['GSI']['index_name']}')
"""
