from services.generation.utility_methods import generate_resource_name


def generate_update_functions(json: dict) -> str:
    """
    This function generates the update functions for a DynamoClass.
    :param json: The json containing the information about the DynamoClass.
    :return: The update functions.
    """
    return f"""{__generate_update_entities_functions(json['entities'])}{__generate_update_links_functions(json['links'])}
{__generate_update_item_method()}
    """


def __generate_update_entities_functions(entities: list) -> str:
    """
    This function generates update functions for entities.
    :param entities: The list of entities to generate update functions for.
    :return: The update functions for the entities.
    """
    return "".join(map(lambda entity: __generate_update_entity_method(generate_resource_name(entity), entity['primary_key'][0]), entities))


def __generate_update_entity_method(entity_name: str, entity_id: str) -> str:
    """
    This function generates the update function for a specific entity.
    :param entity_name: The name of the entity.
    :param entity_id: The ID of the entity.
    :return: The update function for the specific entity.
    """
    return f"""
    def update_{entity_name.lower()}(self, arguments: dict) -> Optional[dict]:
        {entity_id} = arguments.pop('{entity_id}')
        return self.__update_item("{entity_name}", arguments, {entity_id})
        """


def __generate_update_links_functions(links: list) -> str:
    """
    This function generates update functions for links.
    :param links: The list of links to generate update functions for.
    :return: The update functions for the links.
    """
    return "".join(map(lambda link: __generate_update_link_method(generate_resource_name(link), link['first_entity'], link['primary_key'][0],
                                                                  link['second_entity'], link['primary_key'][1]), links))


def __generate_update_link_method(link_name: str, first_entity_name: str, first_entity_id: str, second_entity_name: str, second_entity_id: str) -> str:
    """
     This function generates the update function for a specific link.
     :param first_entity_name: The name of the first entity in the link.
     :param first_entity_id: The ID of the first entity in the link.
     :param second_entity_name: The name of the second entity in the link.
     :param second_entity_id: The ID of the second entity in the link.
     :return: The update function for the specific link.
     """
    return f"""
    def update_link_{first_entity_name.lower()}_{second_entity_name.lower()}(self, arguments: dict) -> Optional[dict]:
        {first_entity_id} = arguments.pop('{first_entity_id}')
        {second_entity_id} = arguments.pop('{second_entity_id}')
        return self.__update_item("{link_name}", arguments, {first_entity_id}, {second_entity_id})
        """


def __generate_update_item_method() -> str:
    """
    This function generates the update function for an item of a DynamoClass.
    :return: The update function for the item.
    """
    return """    def __update_item(self, name: str, arguments: dict, first_entity_id: str, second_entity_id: Optional[str] = None) -> Optional[dict]:
        partition_key = create_id(name, first_entity_id, self.get_configuration().get_separator())
        sort_key = create_id(name, second_entity_id, self.get_configuration().get_separator())
        
        if not self.get_item(partition_key, sort_key):
            raise ItemNotPresentError(name)
        
        response = self.get_configuration().get_table().update_item(
            Key=create_arguments(self.get_configuration().get_storage_keyword(),
                                 self.get_configuration().get_pk_table(),
                                 self.get_configuration().get_sk_table(), partition_key, sort_key),
            UpdateExpression=create_update_expression(arguments),
            ExpressionAttributeValues=create_expression_attribute_values(arguments),
            ReturnValues='ALL_NEW'
        )
        return response['Attributes'] if 'Attributes' in response else None"""
