from Services.Generation.utility_methods import generate_resource_name


def generate_create_functions(json: dict) -> str:
    """
    This function is used to generate the create functions.
    :param json: The json to generate the create functions for.
    :return: The functions as a string.
    """
    return f"""{__generate_create_entities_functions(json['entities'])}
{__generate_create_links_functions(json['links'])}
{__generate_put_item()}"""


def __generate_create_entities_functions(entities: list) -> str:
    """
    This function is used to generate the create functions for the entities.
    :param entities: The entities to generate the create functions for.
    :return: The functions as a string.
    """
    return "".join(map(lambda entity: __generate_create_entity_function(entity), entities))


def __generate_create_links_functions(links: list) -> str:
    """
    This function is used to generate the create functions for the links.
    :param links: The links to generate the create functions for.
    :return: The functions as a string.
    """
    return "".join(map(lambda link: __generate_create_link_function(link), links))


def __generate_create_entity_function(entity: dict) -> str:
    """
    This function is used to generate the create function for an entity.
    :param entity: The entity to generate the create function for.
    :return: The function generated.
    """
    entity_name = generate_resource_name(entity)
    entity_id = entity['primary_key'][0]
    return f"""
    def create_{entity_name.lower()}(self, arguments: dict) -> tuple:
        {entity_name.lower()} = {entity_name}(**arguments)
        return self.__put_item({entity_name.lower()}, "{entity_name}", "{entity_id}"), self.__getAttr({entity_name.lower()}, "{entity_id}")
        """


def __generate_create_link_function(link: dict) -> str:
    """
    This function is used to generate the create function for a link.
    :param link: The link to generate the create function for.
    :return: The function generated.
    """
    link_name = generate_resource_name(link)
    first_entity_name = link['first_entity']
    first_entity_id = link['primary_key'][0]
    second_entity_name = link['second_entity']
    second_entity_id = link['primary_key'][1]
    return f"""
    def create_link_{first_entity_name.lower()}_{second_entity_name.lower()}(self, arguments: dict) -> dict:
        return self.__put_item(
            {link_name}(**arguments),
            "{first_entity_name}",
            "{first_entity_id}",
            "{second_entity_name}",
            "{second_entity_id}"
        )
        """


def __create_link_function() -> str:
    """
    This function is used to create a link function.
    :return: The function.
    """
    return """
    def create_link_{function_name}(self, arguments: dict) -> dict:
        return self.__put_item(
            {link_name}(**arguments),
            "{first_entity}",
            "{first_entity_id}",
            "{second_entity}",
            "{second_entity_id}"
        )
    """


def __generate_put_item() -> str:
    """
    This function is used to put an item in the database.
    :return: The function as a string.
    """
    return """    def __put_item(self, item, name_first_entity: str, first_entity_id_key: str, name_second_entity=None, second_entity_id_key=None) -> dict:
        first_id_entity_to_put = self.create_id(name_first_entity, self.__getAttr(item, first_entity_id_key))
        second_id_entity_to_put = self.create_id(name_second_entity, self.__getAttr(item, second_entity_id_key)) if (name_second_entity and second_entity_id_key) is not None else None
        if self.get_item(first_id_entity_to_put, second_id_entity_to_put):
            raise IdAlreadyExistsError(name_first_entity)

        arguments_to_put = self.__remove_values(item.model_dump(), [f'{first_entity_id_key}', f'{second_entity_id_key}'])
        arguments_to_put.update(self.__create_arguments(first_id_entity_to_put, second_id_entity_to_put))
        return self._table.put_item(Item=arguments_to_put)"""
