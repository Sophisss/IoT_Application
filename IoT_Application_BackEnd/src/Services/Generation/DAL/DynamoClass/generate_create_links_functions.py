from Services.Generation.utility_methods import generate_resource_name


def generate_create_links_functions(links: dict) -> str:
    """
    This method generates the create links functions.
    :param links: The links that need to be created.
    :return: The create links functions.
    """
    returns = ""
    for link in links:
        returns += __generate_create_link(link)
    returns += __generate_put_link()
    return returns


def __generate_create_link(link: dict) -> str:
    """
    This method generates a create link function.
    :param link: The link that needs to be created.
    :return: The create link function.
    """
    first_entity = link['first_entity']
    second_entity = link['second_entity']
    first_entity_id = link['primary_key'][0]
    second_entity_id = link['primary_key'][1]
    return f"""
    def create_link_{first_entity.lower()}_{second_entity.lower()}(self, arguments: dict) -> dict:
        link = {generate_resource_name(link)}(**arguments)
        return self.__put_link(link, "{first_entity}", "{second_entity}", link.{first_entity_id}, link.{second_entity_id})
    """


def __generate_put_link() -> str:
    """
    This method generates the put link function.
    :return: The put link function.
    """
    return """
    def __put_link(self, link, name_first_entity: str, name_second_entity: str, first_entity_id,
                   second_entity_id) -> dict:
        id_first_entity = self.create_id(name_first_entity, first_entity_id)
        id_second_entity = self.create_id(name_second_entity, second_entity_id)
        arguments_to_put = self.__remove_null_values(link.model_dump(), [f'{name_first_entity}_id'.lower(),
                                                                       f'{name_second_entity}_id'.lower()])
        arguments_to_put.update(self.__create_arguments(id_first_entity, id_second_entity))
        return self._table.put_item(Item=arguments_to_put)
    """