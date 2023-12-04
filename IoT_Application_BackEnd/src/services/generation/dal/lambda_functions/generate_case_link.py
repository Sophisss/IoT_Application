def generate_case_link(link):
    name = f"{link['first_entity']}_{link['second_entity']}"
    name_ = f"{link['first_entity']}{link['second_entity']}"
    partition_key = link['primary_key'][0]
    sort_key = link['primary_key'][1]

    api_mapping = {
        'PUT': lambda api: generator_case_put(name, api['name'], name_),
        'DELETE': lambda api: generator_case_delete(name, api['name'], partition_key, sort_key),
        'GET': lambda api: generator_case_get(name, api['name'], partition_key, sort_key),
        'POST': lambda api: generator_case_post(name, api['name']),
    }

    return ''.join([api_mapping[api['type']](api) for api in link['API']]) + default_case()


def generator_case_put(name, api_name, name_):
    return f"""
            case '{api_name}':
                response = project_manager.create_link_{name.lower()}({name_}(**event_parse.arguments['{name_}']))
"""


def generator_case_delete(name, api_name, partition_key, sort_key):
    return f"""
            case '{api_name}':
                response = project_manager.delete_link_{name.lower()}(event_parse.arguments['{partition_key}'],
                                                                       event_parse.arguments['{sort_key}'])
                response = response['Attributes']
"""


def generator_case_get(name, api_name, partition_key, sort_key):
    return f"""
            case '{api_name}':
                response = project_manager.get_{name.lower()}(event_parse.arguments['{partition_key}'],
                                                               event_parse.arguments['{sort_key}'])
                check_response_item(response)
                response = response['Item']
"""


def generator_case_post(name, api_name):
    return f"""
            case '{api_name}':
                response = project_manager.update_link_{name.lower()}(event_parse.arguments)
                response = response['Attributes']
"""


def default_case():
    return f"""
            case _:
                raise InvalidAPIError(event_parse.field)"""
