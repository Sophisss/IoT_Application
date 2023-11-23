from Services.Generation.utility_methods import generate_resource_name


def generate_update_functions(json: dict) -> str:
    """
    This function generates the update functions for a DynamoClass.
    :param json: The json containing the information about the DynamoClass.
    :return: The update functions.
    """
    return f"""{__generate_update_entities_functions(json['entities'])}
{__generate_update_links_functions(json['links'])}
{__generate_update_item()}
    """


def __generate_update_entities_functions(entities: list) -> str:
    """
    This function generates the update functions for the entities of a DynamoClass.
    :param entities: The entities of the DynamoClass.
    :return: The update functions for the entities.
    """
    returns = ""
    for entity in entities:
        returns += __generate_update_entity_function(entity)
    return returns


def __generate_update_links_functions(links: list) -> str:
    """
    This function generates the update functions for the links of a DynamoClass.
    :param links: The links of the DynamoClass.
    :return: The update functions for the links.
    """
    returns = ""
    for link in links:
        returns += __generate_update_link_function(link)
    return returns


def __generate_update_entity_function(entity: dict) -> str:
    """
    This function generates the update function for an entity of a DynamoClass.
    :param entity: The entity of the DynamoClass.
    :return: The update function for the entity.
    """
    entity_name = generate_resource_name(entity)
    entity_id = entity['primary_key'][0]
    return f"""
    def update_{entity_name.lower()}(self, arguments: dict) -> Optional[dict]:
        {entity_id} = arguments.pop('{entity_id}')
        return self.__update_item("{entity_name}", arguments, {entity_id})
        """


def __generate_update_link_function(link: dict) -> str:
    """
    This function generates the update function for a link of a DynamoClass.
    :param link: The link of the DynamoClass.
    :return: The update function for the link.
    """
    link_name = generate_resource_name(link)
    first_entity_name = link['first_entity']
    first_entity_id = link['primary_key'][0]
    second_entity_name = link['second_entity']
    second_entity_id = link['primary_key'][1]
    return f"""
    def update_link_{first_entity_name}_{second_entity_name}(self, arguments: dict) -> Optional[dict]:
        {first_entity_id} = arguments.pop('{first_entity_id}')
        {second_entity_id} = arguments.pop('{second_entity_id}')
        return self.__update_item("{link_name}", arguments, {first_entity_id}, {second_entity_id})
        """


def __generate_update_item() -> str:
    """
    This function generates the update function for an item of a DynamoClass.
    :return: The update function for the item.
    """
    return """    def __update_item(self, name, arguments, partition_key: str, sort_key=None):
        pk = self.create_id(name, partition_key)
        sk = self.create_id(name, sort_key) if sort_key is not None else sort_key
        if not self.get_item(pk, sk):
            raise ItemNotPresentError(name)
        response = self._table.update_item(
            Key=self.__create_arguments(pk, sk),
            UpdateExpression=self.create_update_expression(arguments),
            ExpressionAttributeValues=self.create_expression_attribute_values(arguments),
            ReturnValues='ALL_NEW'
        )
        return response['Attributes'] if 'Attributes' in response else None"""
