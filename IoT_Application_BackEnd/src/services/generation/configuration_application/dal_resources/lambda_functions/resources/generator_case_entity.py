from services.generation.utility_methods import generate_resource_name, get_links_associated


def generate_case_entity(entity: dict, links: list, condition_get: str, condition_get_all: str) -> str:
    """
    This method generates the case of the entity.
    :param entity: entity for which to generate the case.
    :param links: list of links.
    :param condition_get:
    :param condition_get_all:
    :return: The case of the entity.
    """
    entity_name = generate_resource_name(entity)
    partition_key = entity['primary_key'][0]
    link_associated_first_entity, link_associated_second_entity = get_links_associated(entity, links)
    to_return = ""

    for api in entity['API']:
        match api['type']:
            case 'PUT':
                to_return += __generate_case_put(entity_name, api['name'], link_associated_first_entity,
                                                 link_associated_second_entity)
            case 'DELETE':
                to_return += __generate_case_delete(entity_name, api['name'], partition_key)
            case 'GET_ALL':
                to_return += __generate_case_get_all(entity_name, api['name'], condition_get_all)
            case 'GET':
                to_return += __generate_case_get(entity_name, api['name'], partition_key, condition_get)
            case 'POST':
                to_return += __generate_case_post(entity_name, api['name'])

    to_return += __generate_default_case()
    return to_return


def __generate_case_put(entity_name: str, api_name: str, link_associated_first_entity: dict,
                        link_associated_second_entity: dict) -> str:
    """
    This method generates the put case of the entity.
    :param entity_name: The name of the entity.
    :param api_name: The name of the api.
    :return: The put case of the entity.
    """
    condition_case = __generate_condition_case(entity_name, link_associated_first_entity, link_associated_second_entity)

    return f"""
            case '{api_name}':
                {entity_name.lower()} = {entity_name}(**event_parse.arguments['{entity_name}'])
                response = project_manager.create_{entity_name.lower()}({entity_name.lower()})
                check_response_status(response)
                {condition_case}
                return "{entity_name} created"
    """


def __generate_condition_case(entity_name: str, link_associated_first_entity: dict,
                              link_associated_second_entity: dict) -> str:
    condition_case = ""
    condition_case += ''.join(
        map(
            lambda link: __generate_condition_many(entity_name.lower(), link['primary_key'][0], link)
            if (link['numerosity'] == 'one-to-many') or (link['numerosity'] == 'many-to-many')
            else __generate_condition(entity_name.lower(), link['primary_key'][0], link),
            link_associated_first_entity
        )
    )

    condition_case += ''.join(
        map(
            lambda link: __generate_condition_many(entity_name.lower(), link['primary_key'][1], link)
            if (link['numerosity'] == 'many-to-one') or (link['numerosity'] == 'many-to-many')
            else __generate_condition(entity_name.lower(), link['primary_key'][1], link),
            link_associated_second_entity
        )
    )
    return condition_case


def __generate_condition_many(entity_name: str, entity_id, link: dict) -> str:
    """
    This method generates the condition of the entity.
    :param entity_name: The name of the entity.
    :param entity_id: The id of the entity.
    :param link: The link associated to the entity.
    :return: The condition of the entity.
    """
    resource = generate_resource_name(link)
    return f"""
                if '{resource}' in event_parse.arguments:
                    for item in event_parse.arguments['{resource}']:
                        response_link = project_manager.create_{link['first_entity'].lower()}_{link['second_entity'].lower()}({resource}(**item, {entity_id}={entity_name}.{entity_id}))
                        check_response_status(response_link)
    """


def __generate_condition(entity_name: str, entity_id, link: dict) -> str:
    """
    This method generates the condition of the entity.
    :param entity_name: The name of the entity.
    :param entity_id: The id of the entity.
    :param link: The link associated to the entity.
    :return: The condition of the entity.
    """
    resource = generate_resource_name(link)
    return f"""
                if '{resource}' in event_parse.arguments:
                    response_link = project_manager.create_{link['first_entity'].lower()}_{link['second_entity'].lower()}({resource}(**event_parse.arguments['{resource}'], {entity_id}={entity_name}.{entity_id}))
                    check_response_status(response_link)
    """


def __generate_case_delete(entity_name: str, api_name: str, partition_key: str) -> str:
    """
    This method generates the delete case of the entity.
    :param entity_name: The name of the entity.
    :param api_name: The name of the api.
    :param partition_key: The name of the partition key.
    :return: The delete case of the entity.
    """
    return f"""
            case '{api_name}':
                response = project_manager.delete_{entity_name.lower()}(event_parse.arguments['{partition_key}'])
                check_response_status(response)

                if 'Attributes' not in response:
                    raise ItemNotPresentError()

                return "{entity_name} deleted"
"""


def __generate_case_get_all(entity_name: str, api_name: str, condition_get_all: str) -> str:
    """
    This method generates the get all case of the entity.
    :param entity_name: The name of the entity.
    :param api_name: The name of the api.
    :return: The get all case of the entity.
    """
    return f"""            
            case '{api_name}':
                response = project_manager.get_all_{entity_name.lower()}()
                if response:
                    for item in response:
                        check_response_status(item)
                {condition_get_all}
                response = [item['Item'] for item in response]                
"""


def __generate_case_post(entity_name: str, api_name: str) -> str:
    """
    This method generates the post case of the entity.
    :param entity_name: The name of the entity.
    :param api_name: The name of the api.
    :return: The post case of the entity.
    """
    return f"""
            case '{api_name}':
                response = project_manager.update_{entity_name.lower()}(event_parse.arguments)
                check_response_status(response)
                return "{entity_name} updated"
"""


def __generate_case_get(entity_name: str, api_name: str, partition_key: str, condition_get) -> str:
    """
    This method generates the get case of the entity.
    :param entity_name: The name of the entity.
    :param api_name: The name of the api.
    :param partition_key: The name of the partition key.
    :return: The get case of the entity.
    """
    return f"""
            case '{api_name}':
                response = project_manager.get_{entity_name.lower()}(event_parse.arguments['{partition_key}'])
                check_response_item(response)
                check_response_status(response)
                response = response['Item']
                {condition_get}"""


def __generate_default_case() -> str:
    """
    This method generates the default case.
    :return: The default case.
    """
    return f"""
            case _:
                raise InvalidApiError(event_parse.field)"""
