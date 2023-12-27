def generate_resource_name(resource: dict) -> str:
    """
    This function generate the resource name.
    :param resource: The resource to generate the name.
    :return: The resource name.
    """
    return resource.get("name") or f"{resource['first_entity']}{resource['second_entity']}"


def get_table_configuration(table_name: str, json_data: dict) -> dict:
    """
    This method gets the configuration of the table.
    :param table_name: The name of the table.
    :param json_data: The JSON schema containing information.
    :return: The configuration of the table.
    """
    tables = json_data['awsConfig']['dynamo']['tables']
    return next(filter(lambda table: table['tableName'] == table_name, tables))


def get_links_associated(entity: dict, links: list) -> tuple:
    """
    This method gets the links associated to the entity.
    :param entity: entity for which to get the links.
    :param links: list of links.
    :return: The links associated to the entity.
    """
    links_associated_first_entity = [link for link in links if link['first_entity'] == entity['name']]
    links_associated_second_entity = [link for link in links if link['second_entity'] == entity['name']]
    return links_associated_first_entity, links_associated_second_entity
