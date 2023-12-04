"""This file is responsible for generating the fields of the link in the schema.graphql file."""

type_mapping = {
    'string': 'String',
    'integer': 'Int',
}


def generate_fields_link(primary_key: dict, fields: list, type_partition_key: str, type_sort_key: str) -> str:
    return (
            generate_fields_primary_key(primary_key[0], primary_key[1], type_partition_key, type_sort_key) +
            (''.join(map(generate_field, fields)) if fields else '')
    )


def generate_fields_primary_key(partition_key: dict, sort_key: dict, type_partition_key: str,
                                type_sort_key: str) -> str:
    return f"""{partition_key}: {type_mapping.get(type_partition_key)}!
{sort_key}: {type_mapping.get(type_sort_key)}!"""


def generate_field(field: dict) -> str:
    return f"""
{field['name']}: {type_mapping.get(field['type']) if 'allowedValues' not in field else f'allowed{field["name"]}'}{'!' if field['required'] else ''}"""
