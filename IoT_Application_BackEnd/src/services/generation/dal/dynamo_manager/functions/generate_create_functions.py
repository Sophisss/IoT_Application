from services.generation.utility_methods import generate_resource_name


def generate_create_functions(json: dict) -> str:
    """
    This function generates create functions for entities and links based on the provided JSON.
    :param json: The JSON containing entity and link information.
    :return: The create functions.
    """
    return f"""{__generate_create_entities_functions(json['entities'])}{__generate_create_links_functions(json['links'])}
{__generate_put_item_method()}"""


def __generate_create_entities_functions(entities: list) -> str:
    """
    This function generates create functions for entities.
    :param entities: The list of entities to generate create functions for.
    :return: The create functions for the entities.
    """
    return "".join(map(lambda entity: __generate_create_entity_method(generate_resource_name(entity), entity['primary_key'][0]), entities))


def __generate_create_entity_method(entity_name: str, entity_id: str) -> str:
    """
    This function generates the create function for a specific entity.
    :param entity_name: The name of the entity.
    :param entity_id: The ID of the entity.
    :return: The create function for the specific entity.
    """
    return f"""
    def create_{entity_name.lower()}(self, {entity_name.lower()}) -> tuple:
        return self.__put_item({entity_name.lower()}, "{entity_name}", "{entity_id}"), self.__getAttr({entity_name.lower()}, "{entity_id}")
    """


def __generate_create_links_functions(links: list) -> str:
    """
    This function generates create functions for links.
    :param links: The list of links to generate create functions for.
    :return: The create functions for the links.
    """
    return "".join(map(lambda link: __generate_create_link_method(link['first_entity'], link['primary_key'][0], link['second_entity'], link['primary_key'][1]), links))


def __generate_create_link_method(first_entity_name: str, first_entity_id: str, second_entity_name: str,
                                  second_entity_id: str) -> str:
    """
     This function generates the create function for a specific link.
     :param first_entity_name: The name of the first entity in the link.
     :param first_entity_id: The ID of the first entity in the link.
     :param second_entity_name: The name of the second entity in the link.
     :param second_entity_id: The ID of the second entity in the link.
     :return: The create function for the specific link.
     """
    return f"""
    def create_link_{first_entity_name.lower()}_{second_entity_name.lower()}(self, link) -> dict:
        return self.__put_item(
            link,
            "{first_entity_name}",
            "{first_entity_id}",
            "{second_entity_name}",
            "{second_entity_id}"
        )
        """


def __generate_put_item_method() -> str:
    """
    This function generates the function used to put an item in the database.
    :return: The generated function as a string.
    """
    return """    def __put_item(self, item, name_first_entity: str, first_entity_id_key: str, name_second_entity=None, second_entity_id_key=None) -> dict:
        first_id_entity_to_put = self.create_id(name_first_entity, self.__getAttr(item, first_entity_id_key))
        second_id_entity_to_put = self.create_id(name_second_entity, self.__getAttr(item, second_entity_id_key)) if (name_second_entity and second_entity_id_key) is not None else None
        if self.get_item(first_id_entity_to_put, second_id_entity_to_put):
            raise IdAlreadyExistsError(name_first_entity)

        arguments_to_put = self.__remove_values(item.model_dump(), [f'{first_entity_id_key}', f'{second_entity_id_key}'])
        arguments_to_put.update(self.__create_arguments(first_id_entity_to_put, second_id_entity_to_put))
        return self.configuration.table.put_item(Item=arguments_to_put)"""
