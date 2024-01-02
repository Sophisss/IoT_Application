from services.generation.utility_methods import generate_resource_name


def generate_case_link(link: dict) -> str:
    """
    This function generates the case of the link.
    :param link: link for which the case is generated.
    :return: the case of the link.
    """
    name = f"{link['first_entity']}_{link['second_entity']}"
    link_name = generate_resource_name(link)
    partition_key, sort_key = link['primary_key'][0], link['primary_key'][1]
    toReturn = ""

    for api in link['API']:
        match api['type']:
            case 'PUT':
                toReturn += __generate_case_put(name, api['name'], link_name)
            case 'DELETE':
                toReturn += __generate_case_delete(name, api['name'], partition_key, sort_key)
            case 'GET':
                toReturn += __generate_case_get(name, api['name'], partition_key, sort_key)
            case 'POST':
                toReturn += __generate_case_post(name, api['name'])

    toReturn += __generate_default_case()
    return toReturn


def __generate_case_put(name: str, api_name: str, link_name: str) -> str:
    """
    This function generates the case of the put method of the link.
    :param name: name of the link.
    :param api_name: name of the api.
    :param link_name: name of the link.
    :return: the case of the put method of the link.
    """
    return f"""
            case '{api_name}':
                response = project_manager.create_{name.lower()}({link_name}(**event_parse.arguments['{link_name}']))
                check_response_status(response)
                return "{name} created"
"""


def __generate_case_delete(link_name: str, api_name: str, partition_key: str, sort_key: str) -> str:
    """
    This function generates the case of the delete method of the link.
    :param link_name: name of the link.
    :param api_name: name of the api.
    :param partition_key: name of the partition key.
    :param sort_key: name of the sort key.
    :return: the case of the delete method of the link.
    """
    return f"""
            case '{api_name}':
                response = project_manager.delete_{link_name.lower()}(event_parse.arguments['{partition_key}'], event_parse.arguments['{sort_key}'])
                
                if 'Attributes' not in response:
                    raise ItemNotPresentError()
                    
                response = response['Attributes']
"""


def __generate_case_get(link_name: str, api_name: str, partition_key: str, sort_key: str) -> str:
    """
    This function generates the case of the get method of the link.
    :param link_name: name of the link.
    :param api_name: name of the api.
    :param partition_key: name of the partition key.
    :param sort_key: name of the sort key.
    :return: the case of the get method of the link.
    """
    return f"""
            case '{api_name}':
                response = project_manager.get_{link_name.lower()}(event_parse.arguments['{partition_key}'], event_parse.arguments['{sort_key}'])
                check_response_item(response)
                check_response_status(response)
                response = response['Item']
"""


def __generate_case_post(link_name: str, api_name: str) -> str:
    """
    This function generates the case of the post method of the link.
    :param link_name: name of the link.
    :param api_name: name of the api.
    :return: the case of the post method of the link.
    """
    return f"""
            case '{api_name}':
                response = project_manager.update_{link_name.lower()}(event_parse.arguments)
                check_response_status(response)
                response = response['Attributes']
"""


def __generate_default_case() -> str:
    """
    This function generates the default case of the link.
    :return: the default case of the link.
    """
    return f"""
            case _:
                raise InvalidApiError(event_parse.field)"""
