from services.generation.utility_methods import generate_resource_name


def generator_project_dynamo_manager(json: dict) -> str:
    return f"""{__generate_header(json)}
    {__generate_class(json)}
    """


def __generate_header(json: dict) -> str:
    return f"""{__generate_header_entities(json)}
{__generate_header_links(json)}
    """


def __generate_header_entities(json: dict) -> str:
    return "".join(map(lambda entity: __generate_header_entity(generate_resource_name(entity)), json['entities']))


def __generate_header_entity(entity_name: str) -> str:
    return f"""from models.{entity_name.lower()} import {entity_name}
    """


def __generate_header_links(json: dict) -> str:
    return "".join(map(lambda link: __generate_header_link(generate_resource_name(link)), json['links']))


def __generate_header_link(link_name: str) -> str:
    return f"""from models.{link_name.lower()} import {link_name}
    """


def __generate_class(json: dict) -> str:
    return f"""
class ProjectDynamoManager(DynamoManager):
    
{__generate_methods(json)}
    """


def __generate_methods(json: dict) -> str:
    pass
