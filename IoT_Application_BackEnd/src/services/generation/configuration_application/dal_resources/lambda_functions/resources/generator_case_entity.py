from services.generation.configuration_application.dal_resources.lambda_functions.resources.generator_case_get_link import \
    generate_case_get_link_first_entity, generate_case_get_link_second_entity
from services.generation.utility_methods import generate_resource_name, get_links_associated


def generate_case_entity(entity: dict, links: list, name_partition_key_table: str, id_separator: str) -> str:
    """
    This method generates the case of the entity.
    :param entity: entity for which to generate the case.
    :param links: list of links.
    :param name_partition_key_table: The name of the partition key of the table.
    :param id_separator: The id separator.
    :return: The case of the entity.
    """
    entity_name = generate_resource_name(entity)
    partition_key = entity['primary_key'][0]
    link_associated_first_entity, link_associated_second_entity = get_links_associated(entity, links)
    toReturn = ""

    for api in entity['API']:
        match api['type']:
            case 'PUT':
                toReturn += __generate_case_put(entity_name, api['name'], link_associated_first_entity,
                                                link_associated_second_entity)
            case 'DELETE':
                toReturn += __generate_case_delete(entity_name, api['name'], partition_key)
            case 'GET_ALL':
                toReturn += __generate_case_get_all(entity_name, api['name'])
            case 'GET':
                toReturn += __generate_case_get(entity_name, api['name'], partition_key, link_associated_first_entity,
                                                link_associated_second_entity, name_partition_key_table, id_separator)
            case 'POST':
                toReturn += __generate_case_post(entity_name, api['name'])

    toReturn += __generate_default_case()
    return toReturn


def __generate_case_put(entity_name: str, api_name: str, link_associated_first_entity: dict,
                        link_associated_second_entity: dict) -> str:
    """
    This method generates the put case of the entity.
    :param entity_name: The name of the entity.
    :param api_name: The name of the api.
    :return: The put case of the entity.
    """
    condition_case = ""

    def __generate_condition(link: dict, id_entity: str, name_entity: str) -> str:
        resource = generate_resource_name(link)
        return f"""
            if {resource} in event_parse.arguments:
                response_link = project_manager.create_{link['first_entity'].lower()}_{link['second_entity'].lower()}({resource})(**event_parse.arguments['{resource}'], {id_entity}={name_entity}.{id_entity}])
                check_response_status(response_link)
        """

    for link_associated in link_associated_first_entity:
        condition_case += __generate_condition(link_associated, link_associated['primary_key'][0], entity_name.lower())

    for link_associated in link_associated_second_entity:
        condition_case += __generate_condition(link_associated, link_associated['primary_key'][1], entity_name.lower())

    return f"""
        case '{api_name}':
            {entity_name.lower()} = {entity_name}(**event_parse.arguments['{entity_name}'])
            response = project_manager.create_{entity_name.lower()}({entity_name.lower()})
            check_response_status(response)
            {condition_case}
            return "{entity_name} created"
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
                       
                response = response['Attributes']
"""


def __generate_case_get_all(entity_name: str, api_name: str) -> str:
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
                response = response['Attributes']
"""


def __generate_case_get(entity_name: str, api_name: str, partition_key: str, links_associated_first_entity: list,
                        links_associated_second_entity: list, name_partition_key_table: str, id_separator: str) -> str:
    """
    This method generates the get case of the entity.
    :param entity_name: The name of the entity.
    :param api_name: The name of the api.
    :param partition_key: The name of the partition key.
    :param links_associated_first_entity: list of links associated to the first entity.
    :param links_associated_second_entity: list of links associated to the second entity.
    :param name_partition_key_table: The name of the partition key of the table.
    :param id_separator: The id separator.
    :return: The get case of the entity.
    """
    return f"""
            case '{api_name}':
                response = project_manager.get_{entity_name.lower()}(event_parse.arguments['{partition_key}'])
                check_response_item(response)
                check_response_status(response)
                response = response['Item']
                {generate_case_get_link_first_entity(links_associated_first_entity, name_partition_key_table, id_separator) if links_associated_first_entity else ''}
                {generate_case_get_link_second_entity(links_associated_second_entity, name_partition_key_table, id_separator) if links_associated_second_entity else ''}
"""


def __generate_default_case() -> str:
    """
    This method generates the default case.
    :return: The default case.
    """
    return f"""
            case _:
                raise InvalidApiError(event_parse.field)"""
