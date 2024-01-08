"""This file is responsible for generating the fields of the link in the schema.graphql file."""
from services.generation.attribute_type import AttributeType


def generate_fields_link(primary_key: dict, fields: list, type_partition_key: str, type_sort_key: str) -> str:
    return (
            generate_fields_primary_key(primary_key[0], primary_key[1], type_partition_key, type_sort_key) +
            (''.join(map(generate_field, fields)) if fields else '')
    )


def generate_fields_primary_key(partition_key: dict, sort_key: dict, type_partition_key: str,
                                type_sort_key: str) -> str:
    return f"""{partition_key}: {AttributeType[type_partition_key].value}!
{sort_key}: {AttributeType[type_sort_key].value}"""


def generate_field(field: dict) -> str:
    return f"""
{field['name']}: {AttributeType[field['type']].value}{'!' if field['required'] else ''}"""
