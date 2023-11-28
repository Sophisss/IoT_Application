"""This file generates the input types of the schema."""
from generate_fields_entity import generate_fields_entity
from generate_fields_link import generate_fields_link
from generate_types_schema import search_types_primary_key_field


def generate_inputs(entities, links):
    return ''.join(map(generate_input_entity, entities)) + ''.join(
        map(lambda link: generate_input_link(entities, link), links))


def generate_input_entity(entity):
    return f"""
input {entity['name']}Input{{
{generate_fields_entity(entity)}}}
"""


def generate_input_link(entities, link):
    return f"""
input {link['first_entity']}{link['second_entity']}Input{{
{generate_fields_link(link['primary_key'], link['fields'], *search_types_primary_key_field(entities, link))}\n}}"""
