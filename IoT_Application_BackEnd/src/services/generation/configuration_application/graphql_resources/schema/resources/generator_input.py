from services.generation.configuration_application.graphql_resources.schema.resources.generator_fields_entity import \
    generate_fields_entity
from services.generation.configuration_application.graphql_resources.schema.resources.generator_fields_link import \
    generate_fields_link
from services.generation.configuration_application.graphql_resources.schema.resources.generator_types_schema import \
    search_types_primary_key_field


def generate_inputs(entities, links) -> str:
    """
    This function generates the inputs of the schema.
    :param entities: entities in the schema.
    :param links: links in the schema.
    :return: the inputs of the schema.
    """
    return (''.join(map(lambda entity: __generate_input_entity(entity), entities)) +
            ''.join(map(lambda link: __generate_input_link(entities, link), links)))


def __generate_input_entity(entity: dict) -> str:
    """
    This function generates the input for an entity.
    :param entity: the entity.
    :return: the input for an entity.
    """
    return f"""
input {entity['name']}Input{{
{generate_fields_entity(entity)}}}
"""


def __generate_input_link(entities: list, link: dict) -> str:
    """
    This function generates the input for a link.
    :param entities: list of entities.
    :param link: the link.
    :return: the input for a link.
    """
    return f"""
input {link['first_entity']}{link['second_entity']}Input{{
{generate_fields_link(link['primary_key'], link['fields'], *search_types_primary_key_field(entities, link))}\n}}"""
