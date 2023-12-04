from services.generation.dal.lambda_functions.generate_case_get_link import generate_case_get_link_first_entity, \
    generate_case_get_link_second_entity


def generate_case_entity(entity, links, name_partition_key_table):
    entity_name = entity['name']
    partition_key = entity['primary_key'][0]
    link_associated_first_entity, link_associated_second_entity = get_links_associated(entity, links)


    api_mapping = {
        'PUT': lambda api: generator_case_put(entity_name, api['name']),
        'DELETE': lambda api: generator_case_delete(entity_name, api['name'], partition_key),
        'GET_ALL': lambda api: generator_case_get_all(entity_name, api['name']),
        'GET': lambda api: generator_case_get(entity_name, api['name'], partition_key, link_associated_first_entity,
                                              link_associated_second_entity, name_partition_key_table),
        'POST': lambda api: generator_case_post(entity_name, api['name']),
    }

    return ''.join([api_mapping[api['type']](api) for api in entity['API']]) + default_case()


def get_links_associated(entity, links):
    links_associated_first_entity = [link for link in links if link['first_entity'] == entity['name']]
    links_associated_second_entity = [link for link in links if link['second_entity'] == entity['name']]
    return links_associated_first_entity, links_associated_second_entity


def generator_case_put(entity_name, api_name):
    return f"""
            case '{api_name}':
                response = project_manager.create_{entity_name.lower()}({entity_name}(**event_parse.arguments['{entity_name}']))
                check_response_status(response)
                return "{entity_name} created"
 """


def generator_case_delete(entity_name, api_name, partition_key):
    return f"""
            case '{api_name}':
                response = project_manager.delete_{entity_name.lower()}(event_parse.arguments['{partition_key}'])
                check_response_status(response)
                response = response['Attributes']
"""


def generator_case_get_all(entity_name, api_name):
    return f"""            
            case '{api_name}':
                response = project_manager.get_all_{entity_name.lower()}
                check_response_item(response)
                check_response_status(response)
                response = [item['Item'] for item in response]                
"""


def generator_case_post(entity_name, api_name):
    return f"""
            case '{api_name}':
                response = project_manager.update_{entity_name.lower()}(event_parse.arguments)
                check_response_status(response)
                response = response['Attributes']
"""


def generator_case_get(entity_name, api_name, partition_key, links_associated_first_entity,
                       links_associated_second_entity, name_partition_key_table):
    return f"""
            case '{api_name}':
                response = project_manager.get_{entity_name.lower()}(event_parse.arguments['{partition_key}'])
                check_response_item(response)
                check_response_status(response)
                response = response['Item']
                {generate_case_get_link_first_entity(links_associated_first_entity, name_partition_key_table) if links_associated_first_entity else ''}
                {generate_case_get_link_second_entity(links_associated_second_entity, name_partition_key_table) if links_associated_second_entity else ''}
"""


def default_case():
    return f"""
            case _:
                raise InvalidAPIError(event_parse.field)"""
