def generator_lambda(entity, link):
    entity_name = entity['name']
    primary_key = entity['primary_key'][0]
    result_lambda = [f"""
{generator_name_lambda(entity['name'])}
    """]
    for api in entity['API']:
        if api['type'] == 'PUT':
            result_lambda.append(generator_case_put(entity_name, api['name'], primary_key))
        elif api['type'] == 'DELETE':
            result_lambda.append(generator_case_delete(entity_name, api['name'], primary_key))
        elif api['type'] == 'GET_ALL':
            result_lambda.append(generator_case_get_all(entity_name, api['name'], primary_key))
        elif api['type'] == 'GET':
            result_lambda.append(generator_case_get(entity_name, api['name'], primary_key, link))
    result_lambda.append(f"""
            case _:
                response = 'error'
""")
    return ''.join(result_lambda)


def generator_name_lambda(name_entity):
    return f"""def lambda_handler_{name_entity}(event, context):
    try:
        match event['field']:"""


def generator_case_put(name_entity, api_name, partition_key):
    return f"""
            case '{api_name}':
                response, id_entity = dynamodb_manager.create_{name_entity.lower()}(event['arguments']['{name_entity}'])
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    response = f"{name_entity} with id {{id_entity}} created"
"""


def generator_case_delete(name_entity, api_name, partition_key):
    return f"""
            case '{api_name}':
                response, device_id = dynamodb_manager.delete_{name_entity.lower()}(event['arguments']['{partition_key})
                if not response:
                    raise ItemNotPresentError('{name_entity}', {partition_key})
                response['{partition_key}'] = response.pop(dynamodb_manager.get_partition_key_table())
"""


def generator_case_get_all(name_entity, api_name, partition_key):
    return f"""
            case '{api_name}':
                response = dynamodb_manager.get_items_with_secondary_index('{name_entity}')
                if not response:
                    raise EntitiesNotPresentError('{name_entity}')
                for item in response:
                    item['{partition_key}'] = item.pop(dynamodb_manager.get_partition_key_table())
"""


def generator_case_get(name_entity, api_name, partition_key, links):
    result_get = [f"""
            case '{api_name}':
                {partition_key} = dynamodb_manager.create_id_entity('{name_entity}', '{partition_key}', event['arguments'])
                response = dynamodb_manager.get_item({partition_key})
                if not response:
                    raise ItemNotPresentError('{name_entity}', {partition_key})
                response['{partition_key}'] = response.pop(dynamodb_manager.get_partition_key_table())
"""]
    for link in links:
        result_get.append(generate_case_link(name_entity, link))
    return ''.join(result_get)


def generate_case_link(name_entity, link):
    if link['second_entity'] == name_entity and link['numerosity'] == 'one-to-many':
        return link_second_entity_one_to_many(link['first_entity'],
                                              link['primary_key'][0], link['primary_key'][1])
    elif link['first_entity'] == name_entity and link['numerosity'] == 'one-to-many':
        return link_first_entity_one_to_many(link['second_entity'], link['primary_key'][0], link['primary_key'][1])
    elif link['second_entity'] == name_entity and link['numerosity'] == 'many-to-one':
        return link_second_entity_many_to_one(link['first_entity'],
                                              link['primary_key'][0], link['primary_key'][1])
    elif link['first_entity'] == name_entity and link['numerosity'] == 'many-to-one':
        return link_first_entity_many_to_one(link['second_entity'], link['primary_key'][0], link['primary_key'][1])


def link_second_entity_one_to_many(first_entity, partition_key, sort_key):
    return f"""
                if '{first_entity}' in event['projection']:
                    res = dynamodb_manager.get_items_with_secondary_index('{first_entity}', {sort_key})
                    res = res[0][dynamodb_manager.get_partition_key_table()]
                    res = dynamodb_manager.get_item(res)
                    res['{partition_key}'] = res.pop(dynamodb_manager.get_partition_key_table())
                    response['{first_entity}'] = res
"""


def link_first_entity_one_to_many(second_entity, partition_key, sort_key):
    return f"""
                if '{second_entity}' in event['projection']:
                    res = dynamodb_manager.get_items({partition_key}, '{second_entity}')
                    items_result = []
                    for item in res:
                        item = dynamodb_manager.get_item(item[dynamodb_manager.get_sort_key_table()])
                        item['{sort_key}'] = item.pop(dynamodb_manager.get_partition_key_table())
                        items_result.append(item)
                    response['{second_entity}'] = items_result
"""


def link_second_entity_many_to_one(first_entity, partition_key, sort_key):
    return f"""
                if '{first_entity}' in event['projection']:  
                    res = dynamodb_manager.get_items_with_secondary_index({sort_key}, '{first_entity}')
                    items_result = []
                    for item in res:
                        item = dynamodb_manager.get_item(item[dynamodb_manager.get_partition_key_table()])
                        item['{partition_key}'] = item.pop(dynamodb_manager.get_partition_key_table())
                        items_result.append(item)
                    response['{first_entity}'] = items_result
"""


def link_first_entity_many_to_one(second_entity, partition_key, sort_key):
    return f"""
                if '{second_entity}' in event['projection']: 
                    res = dynamodb_manager.get_items({partition_key}, '{second_entity}')
                    res = res[0]
                    res['{sort_key} = item.pop(dynamodb_manager.get_sort_key_table())
                    response['{second_entity}'] = res               
"""
