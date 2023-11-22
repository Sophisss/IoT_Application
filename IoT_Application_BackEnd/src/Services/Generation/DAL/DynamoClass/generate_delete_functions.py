from Services.Generation.utility_methods import generate_resource_name


def generate_delete_functions(json: dict) -> str:
    """
    This function generates the code for the delete functions.
    :param json: The json that contains the information.
    :return: The code for the delete functions.
    """
    return f"""{__generate_delete_entities_functions(json['entities'])}
{__generate_delete_links_functions(json['links'])}
{__generate_delete_item()}
    """


def __generate_delete_entities_functions(entities: list) -> str:
    """
    This function generates the code for the delete_entities_functions.
    :param entities: The entities that need to be deleted.
    :return: The code for the delete_entities_functions.
    """
    returns = ""
    for entity in entities:
        returns += __generate_delete_entity_function(entity)
    return returns


def __generate_delete_links_functions(links: list) -> str:
    """
    This function generates the code for the delete_links_functions.
    :param links: The links that need to be deleted.
    :return: The code for the delete_links_functions.
    """
    returns = ""
    for link in links:
        returns += __generate_delete_link_function(link)
    return returns


def __generate_delete_entity_function(entity: dict) -> str:
    """
    This function generates the code for the delete_entity function.
    :param entity: The entity that needs to be deleted.
    :return: The code for the delete_entity function.
    """
    entity_name = generate_resource_name(entity)
    entity_id = entity['primary_key'][0]
    return f"""
    def delete_{entity_name.lower()}(self, {entity_id}: str) -> tuple[Optional[dict], str]:
        return self.__delete_item({entity_id}), {entity_id}
    """


def __generate_delete_link_function(link: dict) -> str:
    """
    This function generates the code for the delete_link function.
    :param link: The link that needs to be deleted.
    :return: The code for the delete_link function.
    """
    first_entity_name = link['first_entity']
    first_entity_id = link['primary_key'][0]
    second_entity_name = link['second_entity']
    second_entity_id = link['primary_key'][1]
    return f"""
    def delete_link_{first_entity_name.lower()}_{second_entity_name.lower()}(self, {first_entity_id}: str, {second_entity_id}: str):
        return self.__delete_item({first_entity_id}, {second_entity_id})
    """


def __generate_delete_item() -> str:
    """
    This function generates the code for the delete_item function.
    :return: The code for the delete_item function.
    """
    return """
    def __delete_item(self, partition_key: str, sort_key=None) -> Optional[dict]:
        response = self._table.delete_item(
            Key=self.__create_arguments(partition_key, sort_key),
            ReturnValues='ALL_OLD'
        )
        return response['Attributes'] if 'Attributes' in response else None
    """
