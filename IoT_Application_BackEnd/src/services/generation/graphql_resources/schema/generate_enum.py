"""This file is responsible for generating the enum in the schema.graphql file."""


def generate_enum(fields: list) -> str:
    """
    Generate enum from fields
    :param fields: list of fields
    :return: enum
    """
    fields_allowed_values = filter(lambda field: 'allowedValues' in field, fields)
    return '\n'.join(map(lambda field_allowed: f"""enum allowed{field_allowed['name']}{{
{enum_values(field_allowed['allowedValues'])}}}\n""", fields_allowed_values))


def enum_values(values: list) -> str:
    """
    Generate enum values
    :param values: list of values
    :return: enum values
    """
    return ''.join(map(lambda value: f"{value}\n", values))
