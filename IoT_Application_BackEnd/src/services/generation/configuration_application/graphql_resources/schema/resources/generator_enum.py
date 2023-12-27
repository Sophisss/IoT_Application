def generate_enum(fields: list) -> str:
    """
    This method generates the enum for the graphql schema.
    :param fields: list of fields.
    :return: enum.
    """
    fields_allowed_values = filter(lambda field: 'allowedValues' in field, fields)
    return '\n'.join(map(lambda field_allowed: f"""enum allowed{field_allowed['name']}{{
{__enum_values(field_allowed['allowedValues'])}}}\n""", fields_allowed_values))


def __enum_values(values: list) -> str:
    """
    This method generates the values of the enum.
    :param values: list of values.
    :return: values of the enum.
    """
    return ''.join(map(lambda value: f"{value}\n", values))
