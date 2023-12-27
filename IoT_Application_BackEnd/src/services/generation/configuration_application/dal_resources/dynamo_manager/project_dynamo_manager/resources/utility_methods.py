from services.generation.utility_methods import generate_resource_name


# region get functions


def get_utility_resources(item: dict) -> tuple:
    """
    This method gets the utility resources of the entity or link.
    :param item: The entity or link.
    :return: The utility resources of the entity or link.
    """
    item_name = generate_resource_name(item)
    item_primary_key = item['primary_key']
    return item_name, item_primary_key


def get_entities_name(link: dict) -> tuple:
    """
    This method returns the name of the entities.
    :param link: The link.
    :return: The name of the entities.
    """
    return link['first_entity'], link['second_entity']

# endregion


def generate_fields(item: dict, item_name: str) -> str:
    """
    This method generates the fields of the entity or link.
    :param item: The entity or link.
    :param item_name: The name of the entity or link.
    :return: The fields of the entity or link.
    """
    partition_key = item['primary_key'][0]
    return ",\n".join(map(lambda field: f"            '{field['name']}': {item_name.lower()}.{field['name']}",
                          filter(lambda field: field["name"] != partition_key, item["fields"])))


def generate_arguments_update(parameters: list) -> str:
    """
    This method generates the arguments of the update method of the entity or link.
    :param parameters: The parameters of the update method.
    :return: The arguments of the update method of the entity or link.
    """
    return ",\n".join(map(lambda parameter: f"                '{parameter}': arguments['{parameter}']", parameters))


def generate_pk_sk_put(item_primary_key: str, table_configuration: dict, first_entity_name: str,
                       second_entity_name=None) -> str:
    """
    This method generates the primary and sort key of the entity or link.
    :param item_primary_key: The primary key of the entity or link.
    :param table_configuration: The configuration of the table.
    :param first_entity_name: The name of the first entity.
    :param second_entity_name: The name of the second entity.
    :return: The primary and sort key of the entity or link.
    """
    if len(item_primary_key) == 2:
        return f"""'{table_configuration['partition_key']['name']}': f'{first_entity_name}{table_configuration['parameters']['id_separator']}{{link.{item_primary_key[0]}}}',
            '{table_configuration['sort_key']['name']}': f'{second_entity_name}{table_configuration['parameters']['id_separator']}{{link.{item_primary_key[1]}}}'"""
    else:
        return f"""'{table_configuration['partition_key']['name']}': f'{first_entity_name}{table_configuration['parameters']['id_separator']}{{{first_entity_name.lower()}.{item_primary_key[0]}}}',
            '{table_configuration['sort_key']['name']}': '{table_configuration['parameters']['single_entity_storage_keyword']}'"""


def generate_pk_sk_update(item_primary_key: str, table_configuration: dict, first_entity_name: str,
                          second_entity_name=None) -> str:
    """
    This method generates the primary and sort key of the entity or link.
    :param item_primary_key: The primary key of the entity or link.
    :param table_configuration: The configuration of the table.
    :param first_entity_name: The name of the first entity.
    :param second_entity_name: The name of the second entity.
    :return: The primary and sort key of the entity or link.
    """
    if len(item_primary_key) == 2:
        return f"""'{table_configuration['partition_key']['name']}': f'{first_entity_name}{table_configuration['parameters']['id_separator']}{{arguments["{item_primary_key[0]}"]}}',
            '{table_configuration['sort_key']['name']}': f'{second_entity_name}{table_configuration['parameters']['id_separator']}{{arguments["{item_primary_key[1]}"]}}'"""
    else:
        return f"""'{table_configuration['partition_key']['name']}': f'{first_entity_name}{table_configuration['parameters']['id_separator']}{{arguments["{item_primary_key[0]}"]}}',
            '{table_configuration['sort_key']['name']}': '{table_configuration['parameters']['single_entity_storage_keyword']}'"""


def generate_pk_sk(item_primary_key: str, table_configuration: dict, first_entity_name: str,
                   second_entity_name=None) -> str:
    """
    This method generates the primary and sort key of the entity or link.
    :param item_primary_key: The primary key of the entity or link.
    :param table_configuration: The configuration of the table.
    :param first_entity_name: The name of the first entity.
    :param second_entity_name: The name of the second entity.
    :return: The primary and sort key of the entity or link.
    """
    if len(item_primary_key) == 2:
        return f"""'{table_configuration['partition_key']['name']}': f'{first_entity_name}{table_configuration['parameters']['id_separator']}{{{item_primary_key[0]}}}',
            '{table_configuration['sort_key']['name']}': f'{second_entity_name}{table_configuration['parameters']['id_separator']}{{{item_primary_key[1]}}}'"""
    else:
        return f"""'{table_configuration['partition_key']['name']}': f'{first_entity_name}{table_configuration['parameters']['id_separator']}{{{item_primary_key[0]}}}',
            '{table_configuration['sort_key']['name']}': '{table_configuration['parameters']['single_entity_storage_keyword']}'"""
