from typing import Optional
from services.generation.utility_methods import generate_resource_name


def generate_header_lambda(name: str, project_name: str, entity_links: Optional = None) -> str:
    """
    This function generates the header of the lambda.
    :param name: name of the entity or link.
    :param project_name: name of the project.
    :param entity_links: links associated to the entity if exists.
    :return: the header of the lambda.
    """
    import_models_link = __generate_import_models_link(entity_links) if entity_links else ""
    return f"""from response_manager.exception_class import *
from dynamo_manager.project_dynamo_manager import IoT_PlatformDynamoManager
from response_manager.response_manager import check_response_status, check_response_item
from dynamo_manager.utility import change_name_keys
from event.event import Event
from event.event_parse import parse_event
from model.{name.lower()} import {name}
{import_models_link}
"""


def __generate_import_models_link(links: list) -> str:
    """
    This function generates the import of the models of the links.
    :param links: links associated to the entity if exists.
    :return: the import of the models of the links.
    """
    import_models_link = ""
    for link in links:
        link_name = generate_resource_name(link)
        import_models_link += f"from model.{link_name.lower()} import {link_name}\n"
    return import_models_link
