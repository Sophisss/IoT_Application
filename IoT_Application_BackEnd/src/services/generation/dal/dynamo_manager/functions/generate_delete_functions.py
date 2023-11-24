from services.generation.utility_methods import generate_resource_name


def generate_delete_functions(json: dict) -> str:
    """
    This function generates the code for the delete functions.
    :param json: The json that contains the information.
    :return: The code for the delete functions.
    """
    return f"""{__generate_delete_entities_functions(json['entities'])}{__generate_delete_links_functions(json['links'])}
{__generate_delete_item()}
{__generate_remove_associated_link()}
{__generate_delete()}"""


def __generate_delete_entities_functions(entities: list) -> str:
    """
    This function generates the code for the delete_entities_functions.
    :param entities: The entities that need to be deleted.
    :return: The code for the delete_entities_functions.
    """
    return "".join(map(lambda entity: __generate_delete_entity_function(entity), entities))


def __generate_delete_links_functions(links: list) -> str:
    """
    This function generates the code for the delete_links_functions.
    :param links: The links that need to be deleted.
    :return: The code for the delete_links_functions.
    """
    return "".join(map(lambda link: __generate_delete_link_function(link), links))


def __generate_delete_entity_function(entity: dict) -> str:
    """
    This function generates the code for the delete_entity function.
    :param entity: The entity that needs to be deleted.
    :return: The code for the delete_entity function.
    """
    entity_name = generate_resource_name(entity)
    entity_id = entity['primary_key'][0]
    return f"""
    def delete_{entity_name.lower()}(self, {entity_id}: str) -> Optional[dict]:
        return self.__delete_item("{entity_name}", {entity_id})
        """


def __generate_delete_link_function(link: dict) -> str:
    """
    This function generates the code for the delete_link function.
    :param link: The link that needs to be deleted.
    :return: The code for the delete_link function.
    """
    link_name = generate_resource_name(link)
    first_entity_name = link['first_entity']
    first_entity_id = link['primary_key'][0]
    second_entity_name = link['second_entity']
    second_entity_id = link['primary_key'][1]
    return f"""
    def delete_link_{first_entity_name.lower()}_{second_entity_name.lower()}(self, {first_entity_id}: str, {second_entity_id}: str):
        return self.__delete_item("{link_name}", {first_entity_id}, {second_entity_id})
        """


def __generate_delete_item() -> str:
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


def __generate_remove_associated_link() -> str:
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


def __generate_delete() -> str:
    """
    This function generates the code for the delete function.
    :return: The code for the delete function.
    """
    return """    def __delete(self, key: dict):
        return self.configuration.table.delete_item(
            Key=key,
            ReturnValues='ALL_OLD'
        )"""
