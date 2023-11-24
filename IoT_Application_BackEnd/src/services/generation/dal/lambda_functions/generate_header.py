from services.generation.utility_methods import generate_resource_name


def generate_header_dal_api(json):  # TODO RIVEDI TABELLE
    """
    This function generates the header for the DAL.
    :param json: The json file.
    :return: The header for the DAL.
    """
    return f"""from configuration import Configuration
from dynamo_class import DynamoManager
from event.event import Event
from event.event_parse import parse_event
from exception_class import IdAlreadyExistsError, ItemNotPresentError, EntitiesNotPresentError
{__generate_header_entities(json['entities'])}{__generate_header_links(json['links'])}
{__generate_dynamo_manager_instance(json['awsConfig']['dynamo']['tables'][0], json['parameters'])}  
    """


def __generate_header_entities(entities: list) -> str:
    """
    This function generates the header for the entities.
    :param entities: The entities that are needed to generate the header.
    :return: The header for the entities.
    """
    return "".join(map(lambda entity: __generate_header_entity(entity), entities))


def __generate_header_entity(entity: dict) -> str:
    """
    This function generates the header for the entity.
    :param entity: The entity that is needed to generate the header.
    :return: The header for the entity.
    """
    entity_name = generate_resource_name(entity)
    return f"""
from model.{entity_name.lower()} import {entity_name}\n
    """


def __generate_header_links(links: list) -> str:
    """
    This function generates the header for the links.
    :param links: The links that are needed to generate the header.
    :return: The header for the links.
    """
    return "".join(map(lambda link: __generate_header_link(link), links))


def __generate_header_link(link: dict) -> str:
    """
    This function generates the header for the link.
    :param link: The link that is needed to generate the header.
    :return: The header for the link.
    """
    link_name = generate_resource_name(link)
    return f"""
from model.{link_name.lower()} import {link_name}\n
    """


def __generate_dynamo_manager_instance(table_details: dict, parameters: dict) -> str:
    """
    This function generates the dynamo manager instance.
    :param table_details: The table details.
    :param parameters: The parameters.
    :return: The dynamo manager instance.
    """
    return f"""dynamodb_manager = DynamoManager(Configuration('{table_details['tableName']}', '{parameters['id_separator']}', '{table_details['partition_key']['name']}', '{table_details['sort_key']['name']}',
                                               '{parameters['single_entity_storage_keyword']}', '{table_details['GSI']['index_name']}'))
    """
