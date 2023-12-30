"""This file is responsible for generating entities and links types in the schema.graphql file."""
from services.generation.configuration_application.graphql_resources.schema.resources.generator_enum import generate_enum
from services.generation.configuration_application.graphql_resources.schema.resources.generator_fields_entity import \
    generate_fields_entity, generate_fields_entity_links
from services.generation.configuration_application.graphql_resources.schema.resources.generator_fields_link import \
    generate_fields_link


def generate_types(entities: list, links: list) -> str:
    return f"""{generate_types_entities(entities, links)}{generate_types_links(entities, links)}"""


def generate_types_entities(entities: list, links: list) -> str:
    return ''.join(map(lambda entity: generate_type_entity(*entity_links(entity, links)), entities))


def generate_type_entity(entity: dict, links: list) -> str:
    return f"""type {entity['name']} {{
{generate_fields_entity(entity)}{generate_fields_entity_links(entity['name'], links) if bool(links) else ''}}}\n
{generate_enum(entity['fields'])}
"""


def entity_links(entity: dict, links: list) -> tuple:
    return entity, list(
        filter(lambda link: link['first_entity'] == entity['name'] or link['second_entity'] == entity['name'], links))


def generate_types_links(entities: list, links: list) -> str:
    return ''.join(map(lambda link: generate_type_link(link, entities), links))


def generate_type_link(link: dict, entities: list) -> str:
    return f"""type {link['first_entity']}{link['second_entity']}{{
{generate_fields_link(link['primary_key'], link['fields'], *search_types_primary_key_field(entities, link))}\n}}\n
{generate_enum(link['fields']) if link['fields'] else ''}
"""


def search_types_primary_key_field(entities: list, link: dict) -> tuple:
    entity_partition_key = next(filter(lambda entity: entity['name'] == link['first_entity'], entities), None)
    type_partition_key = next(
        filter(lambda field: field['name'] == link['primary_key'][0], entity_partition_key['fields']), None)
    entity_sort_key = next(filter(lambda entity: entity['name'] == link['second_entity'], entities), None)
    type_sort_key = next(filter(lambda field: field['name'] == link['primary_key'][1], entity_sort_key['fields']),
                         None)
    return type_partition_key['type'], type_sort_key['type']
