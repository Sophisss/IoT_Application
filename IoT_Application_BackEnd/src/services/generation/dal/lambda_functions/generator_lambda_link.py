def generator_lambda_link(link):
    first_entity = link['first_entity']
    second_entity = link['second_entity']
    partition_key = link['primary_key'][0]
    sort_key = link['primary_key'][1]
    result_link = [f"""
{generator_header_lambda_link(first_entity, second_entity)}
"""]
    for api in link['API']:
        if api['type'] == 'PUT':
            result_link.append(generator_case_put_link(api['name'], first_entity, second_entity))
        elif api['type'] == 'DELETE':
            result_link.append(
                generator_case_delete_link(api['name'], first_entity, second_entity, partition_key, sort_key))
        elif api['type'] == 'GET':
            result_link.append(
                generator_case_get_link(api['name'], first_entity, second_entity, partition_key, sort_key))
        elif api['type'] == 'POST':
            result_link.append(generator_case_update_link(api['name'], partition_key, sort_key))
    return ''.join(result_link)


def generator_header_lambda_link(first_entity, second_entity):
    return f"""@parse_event(Event)
def lambda_handler_{first_entity}{second_entity}(event, context,event_parse: Event):
     match event_parse.field:"""


def generator_case_put_link(api_name, first_entity, second_entity):
    return f"""
        case '{api_name}':
            response = dynamodb_manager.create_link_{first_entity.lower()}_{second_entity.lower()}(**event_parse.arguments)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                response = f"Link created"
    """


def generator_case_delete_link(api_name, first_entity, second_entity, partition_key, sort_key):
    return f"""
        case '{api_name}':
            response = dynamodb_manager.delete_link_{first_entity.lower()}_{second_entity.lower()}(event_parse.arguments['{partition_key}'], event_parse.arguments['{sort_key}'])
            response['{partition_key}'] = response.pop(dynamodb_manager.get_partition_key_table())
            response['{sort_key}'] = response.pop(dynamodb_manager.get_sort_key_table())
            response = list(response.values())
"""


def generator_case_get_link(api_name, first_entity, second_entity, partition_key, sort_key):
    return f"""
        case '{api_name}':
            {partition_key} = dynamodb_manager.create_id('{first_entity}',event_parse.arguments['{partition_key}'])
            {sort_key} = dynamodb_manager.create_id('{second_entity}',event['arguments']['{sort_key}'])
            response = dynamodb_manager.get_item({partition_key}, {sort_key})
            response['{partition_key}'] = response.pop(dynamodb_manager.get_partition_key_table())
            response['{sort_key}'] = response.pop(dynamodb_manager.get_sort_key_table())
            response = list(response.values())
"""


def generator_case_update_link(api_name, partition_key, sort_key):
    return f"""
        case '{api_name}':
            response = dynamodb_manager.update_device(event_parse.arguments)
            if not response:
                raise ItemNotPresentError('Link')
            else:
                response['{partition_key}'] = response.pop(dynamodb_manager.get_partition_key_table())
                response['{sort_key}'] = response.pop(dynamodb_manager.get_sort_key_table())
"""

