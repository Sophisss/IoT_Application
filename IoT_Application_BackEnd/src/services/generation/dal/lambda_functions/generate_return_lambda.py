def generate_return_lambda_entity(name_partition_key_field, name_partition_key_table):
    return f"""
    return change_name_keys(response, ('{name_partition_key_field}', '{name_partition_key_table}'))
"""


def generate_return_lambda_link(name_partition_key_field, name_partition_key_table, name_sort_key_field,
                                name_sort_key_table):
    return f"""
    return change_name_keys(response, ('{name_partition_key_field}', '{name_partition_key_table}'), ('{name_sort_key_field}', '{name_sort_key_table}'))"""
