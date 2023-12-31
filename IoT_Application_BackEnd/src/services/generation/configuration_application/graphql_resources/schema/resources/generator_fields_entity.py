"""This file is responsible for generating the fields of an entity in the schema.graphql file."""
from services.generation.attribute_type import AttributeType


def generate_fields_entity(entity: dict) -> str:
    return ''.join(map(generate_field, entity['fields']))


def generate_fields_entity_links(name_entity: str, list_link: list) -> str:
    return ''.join(map(lambda link: generate_field_link(name_entity, link), list_link))


def generate_field(field: dict) -> str:
    return f"""{field['name']}: {AttributeType[field['type']].value}{'!' if field['required'] else ''}\n"""


def generate_field_link(name_entity: str, link: dict) -> str:
    mapping = {
        ('one-to-many', True): '{name}:[{name_type}]\n',
        ('many-to-one', True): '{name}:{name_type}\n',
        ('one-to-many', False): '{name}:{name_type}\n',
        ('many-to-one', False): '{name}:[{name_type}]\n',
        ('many-to-many', True): '{name}:[{name_type}]\n',
        ('many-to-many', False): '{name}:[{name_type}]\n',
        ('one-to-one', True): '{name}:{name_type}\n',
        ('one-to-one', False): '{name}:{name_type}\n',
    }
    first_entity, second_entity, numerosity = link['first_entity'], link['second_entity'], link['numerosity']
    name, name_type = (second_entity, second_entity) if name_entity == first_entity else (first_entity, first_entity)
    output_format = mapping.get((numerosity, name_entity == first_entity), '{name}:{name_type}')
    return output_format.format(name=name, name_type=name_type)
