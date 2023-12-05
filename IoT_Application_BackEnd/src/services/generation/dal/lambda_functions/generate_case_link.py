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
                response = project_manager.create_{name.lower()}({name_}(**event_parse.arguments['{name_}']))
                check_response_status(response)
                return "{name} created"
"""


def generator_case_delete(name, api_name, partition_key, sort_key):
    return f"""
            case '{api_name}':
                response = project_manager.delete_{name.lower()}(event_parse.arguments['{partition_key}'], event_parse.arguments['{sort_key}'])
                
                if 'Attributes' not in response:
                       raise ItemNotPresentError()
                    
                response = response['Attributes']
"""


def generator_case_get(name, api_name, partition_key, sort_key):
    return f"""
            case '{api_name}':
                response = project_manager.get_{name.lower()}(event_parse.arguments['{partition_key}'], event_parse.arguments['{sort_key}'])
                check_response_item(response)
                check_response_status(response)
                response = response['Item']
"""


def generator_case_post(name, api_name):
    return f"""
            case '{api_name}':
                response = project_manager.update_{name.lower()}(event_parse.arguments)
                check_response_status(response)
                response = response['Attributes']
"""


def default_case():
    return f"""
            case _:
                raise InvalidApiError(event_parse.field)"""
