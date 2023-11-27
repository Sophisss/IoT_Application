def generate_case_link(link):
    name = f"{link['first_entity']}{link['second_entity']}"
    partition_key = link['primary_key'][0]
    sort_key = link['primary_key'][1]

    api_mapping = {
        'PUT': lambda api: generator_case_put(name, api['name']),
        'DELETE': lambda api: generator_case_delete(name, api['name'], partition_key, sort_key),
        'GET': lambda api: generator_case_get(name, api['name'], partition_key, sort_key),
        'POST': lambda api: generator_case_post(name, api['name'], partition_key),
    }

    return ''.join([api_mapping[api['type']](api) for api in link['API']]) + default_case()


def generator_case_put(name, api_name):
    return f"""
            case '{api_name}':
                response = dynamodb_manager.create_link_{name.lower()}({name}(**event_parse.arguments['{name}']))
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    response = f"Link created"
    """


def generator_case_delete(name, api_name, partition_key, sort_key):
    return f"""
            case '{api_name}':
                response = dynamodb_manager.delete_link_{name.lower()}(event_parse.arguments['{partition_key}']
                                                                       event_parse.arguments['{sort_key}'])
                if not response:
                    raise ItemNotPresentError('{name}')
                response['{partition_key}'] = response.pop(dynamodb_manager.get_configuration().get_pk_table())
                resposne['{sort_key}'] = response.pop(dynamodb_managerget_configuration().get_sk_table())
    """


def generator_case_get(name, api_name, partition_key, sort_key):
    return f"""
            case '{api_name}':
                {partition_key} = dynamodb_manager.create_id('{name}',event_parse.arguments['{partition_key}'])
                {sort_key} = dynamodb_manager.create_id('{name}',event_parse.arguments['{sort_key}'])
                response = dynamodb_manager.get_item({partition_key}, {sort_key})
                response['{partition_key}'] = response.pop(dynamodb_manager.get_configuration().get_pk_table())
                response['{sort_key}'] = response.pop(dynamodb_managerget_configuration().get_sk_table())
               
"""


def generator_case_post(name, api_name, partition_key, sort_key):
    return f"""
            case '{api_name}':
                response = dynamodb_manager.update_link_{name.lower()}(event_parse.arguments)
                if not response:
                    raise ItemNotPresentError('{name}')
                else:
                    response['{partition_key}'] = response.pop(dynamodb_manager.get_configuration().get_pk_table())
                    response['{sort_key}'] = response.pop(dynamodb_managerget_configuration().get_sk_table())
"""


def default_case():
      return f"""
            case _:
                raise InvalidAPIError(event_parse.field)"""


