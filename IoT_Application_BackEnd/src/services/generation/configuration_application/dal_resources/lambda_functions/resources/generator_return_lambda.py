def generate_return_lambda_entity(name_partition_key_field: str, name_partition_key_table: str, separator: str) -> str:
    """
    This method generates the return of the lambda of the entity.
    :param name_partition_key_field: name of the partition key field.
    :param name_partition_key_table: name of the partition key table.
    :param separator: separator of the id.
    :return: the return of the lambda of the entity.
    """
    return f"""
    return change_name_keys(response, ('{name_partition_key_field}', '{name_partition_key_table}', '{separator}'))
"""


def generate_return_lambda_link(name_partition_key_field: str, name_partition_key_table: str, name_sort_key_field: str,
                                name_sort_key_table: str, separator: str) -> str:
    """
    This method generates the return of the lambda of the link.
    :param name_partition_key_field: name of the partition key field.
    :param name_partition_key_table: name of the partition key table.
    :param name_sort_key_field: name of the sort key field.
    :param name_sort_key_table: name of the sort key table.
    :param separator: separator of the id.
    :return: the return of the lambda of the link.
    """
    return f"""
    return change_name_keys(response, ('{name_partition_key_field}', '{name_partition_key_table}', '{separator}'), ('{name_sort_key_field}', '{name_sort_key_table}', '{separator}'))"""
