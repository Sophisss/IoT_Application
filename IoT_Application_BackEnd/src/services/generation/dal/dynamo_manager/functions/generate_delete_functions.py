from services.generation.utility_methods import generate_resource_name


def generate_delete_functions(json: dict) -> str:
    """
    This function generates delete functions for entities and links based on the provided JSON.
    :param json: The JSON containing entity and link information.
    :return: The delete functions.
    """
    return f"""{__generate_delete_entities_functions(json['entities'])}{__generate_delete_links_functions(json['links'])}
{__generate_delete_item_method()}
{__generate_remove_associated_link_method()}
{__generate_delete_method()}"""


def __generate_delete_entities_functions(entities: list) -> str:
    """
    This function generates delete functions for entities.
    :param entities: The list of entities to generate delete functions for.
    :return: The delete functions for the entities.
    """
    return "".join(map(lambda entity: __generate_delete_entity_method(generate_resource_name(entity), entity['primary_key'][0]), entities))


def __generate_delete_entity_method(entity_name: str, entity_id: str) -> str:
    """
    This function generates the delete function for a specific entity.
    :param entity_name: The name of the entity.
    :param entity_id: The ID of the entity.
    :return: The delete function for the specific entity.
    """
    return f"""
    def delete_{entity_name.lower()}(self, {entity_id}: str) -> Optional[dict]:
        return self.__delete_item("{entity_name}", {entity_id})
        """


def __generate_delete_links_functions(links: list) -> str:
    """
    This function generates delete functions for links.
    :param links: The list of links to generate delete functions for.
    :return: The delete functions for the links.
    """
    return "".join(map(lambda link: __generate_delete_link_method(generate_resource_name(link), link['first_entity'], link['primary_key'][0],
                                                                  link['second_entity'], link['primary_key'][1]), links))


def __generate_delete_link_method(link_name: str, first_entity_name: str, first_entity_id: str, second_entity_name: str,
                                  second_entity_id: str) -> str:
    """
    This function generates the delete function for a specific link.
    :param link_name: The name of the link.
    :param first_entity_name: The name of the first entity in the link.
    :param first_entity_id: The ID of the first entity in the link.
    :param second_entity_name: The name of the second entity in the link.
    :param second_entity_id: The ID of the second entity in the link.
    :return: The delete function for the specific link.
    """
    return f"""
    def delete_link_{first_entity_name.lower()}_{second_entity_name.lower()}(self, {first_entity_id}: str, {second_entity_id}: str):
        return self.__delete_item("{link_name}", {first_entity_id}, {second_entity_id})
        """


def __generate_delete_item_method() -> str:
    """
    This function generates the code for the delete_item function.
    :return: The code for the delete_item function.
    """
    return """    def __delete_item(self, name, partition_key: str, sort_key=None) -> Optional[dict]:
        pk = self.create_id(name, partition_key)
        sk = self.create_id(name, sort_key) if sort_key is not None else sort_key
        response = self.__delete(self.__create_arguments(pk, sk))
        self.__remove_associated_link(pk)
        return response['Attributes'] if 'Attributes' in response else None
    """


def __generate_remove_associated_link_method() -> str:
    """
    This function generates the code for the remove_associated_link function.
    :return: The code for the remove_associated_link function.
    """
    return """    def __remove_associated_link(self, item_id):
        response = self.get_items(item_id)

        if response is not None:
            for item in response:
                key = self.__create_arguments(item[self.get_partition_key_table()], item[self.get_sort_key_table()])
                self.__delete(key)

        response = self.get_items_with_secondary_index(key=item_id)

        if response is not None:
            for item in response:
                key = self.__create_arguments(item[self.get_partition_key_table()], item[self.get_sort_key_table()])
                self.__delete(key)
    """


def __generate_delete_method() -> str:
    """
    This function generates the code for the delete function.
    :return: The code for the delete function.
    """
    return """    def __delete(self, key: dict):
        return self.configuration.table.delete_item(
            Key=key,
            ReturnValues='ALL_OLD'
        )"""
