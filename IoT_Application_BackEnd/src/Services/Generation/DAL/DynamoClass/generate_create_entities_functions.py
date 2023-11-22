def generate_create_entities_functions(entities: dict) -> str:
    """
    This function generates the code for the create entities functions.
    :param entities: The entities that need to be created.
    :return: The code for the create entities functions.
    """
    returns = ""
    for entity in entities:
        returns += __generate_create_entity(entity)
    returns += __generate_put_entity()
    return returns


def __generate_create_entity(entity: dict) -> str:
    """
    This function generates the code for the create entity function.
    :param entity: The entity that needs to be created.
    :return: The code for the create entity function.
    """
    entity_name = entity['name']
    entity_id = f"{entity_name.lower()}.{entity['primary_key'][0]}"
    return f"""
    def create_{entity_name.lower()}(self, arguments: dict) -> tuple:
        {entity_name.lower()} = {entity_name}(**arguments)
        return self.__put_entity("{entity_name}", {entity_id}, {entity_name.lower()}), {entity_id}
    """


def __generate_put_entity() -> str:
    """
    This function generates the code for the put entity function.
    :return: The code for the put entity function.
    """
    return """
    def __put_entity(self, name: str, entity_id, entity) -> dict:
        id_entity = self.create_id(name, entity_id)
        if self.get_item(id_entity):
            raise IdAlreadyExistsError(name, id_entity)

        arguments_to_put = self.__remove_null_values(entity.model_dump(), [f'{name}_id'.lower()])
        arguments_to_put.update(self.__create_arguments(id_entity))
        return self._table.put_item(Item=arguments_to_put)
        """
