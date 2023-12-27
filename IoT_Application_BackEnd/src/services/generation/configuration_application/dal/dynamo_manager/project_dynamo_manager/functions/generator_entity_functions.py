from services.generation.configuration_application.dal.dynamo_manager.project_dynamo_manager.functions.generate_entity_relation import \
    generate_entity_relation
from services.generation.configuration_application.dal.dynamo_manager.project_dynamo_manager.functions.utility import \
    get_table_configuration, get_utility_resources, generate_pk_sk_put, generate_fields, generate_pk_sk, \
    generate_arguments_update, generate_pk_sk_update


def generate_entity_methods(entity: dict, json_data: dict) -> str:
    """
    This method generates the methods of the entity.
    :param entity: The entity.
    :param json_data: The JSON schema containing information.
    :return: The methods of the entity.
    """
    table_configuration = get_table_configuration(entity['table'], json_data)
    return ("".join(map(lambda api: __generate_entity_api_method(entity, api, table_configuration), entity['API'])) +
            generate_entity_relation(entity, json_data['links'], table_configuration))


def __generate_entity_api_method(entity: dict, api: dict, table_configuration: dict) -> str:
    """
    This method generates the methods of the entity.
    :param entity: The entity.
    :param api: The API.
    :param table_configuration: The configuration of the table.
    :return: The methods of the entity.
    """
    methods_to_return = ""
    match api['type']:
        case 'GET':
            methods_to_return += __generate_get_entity_method(entity, table_configuration)
        case 'GET_ALL':
            methods_to_return += __generate_get_entities_method(entity, table_configuration)
        case 'POST':
            methods_to_return += __generate_update_method(entity, table_configuration, api)
        case 'PUT':
            methods_to_return += __generate_create_method(entity, table_configuration)
        case 'DELETE':
            methods_to_return += __generate_delete_method(entity, table_configuration)
    return methods_to_return


def __generate_create_method(entity: dict, table_configuration: dict) -> str:
    """
    This method generates the create method of the entity.
    :param entity: The entity.
    :param table_configuration: The configuration of the table.
    :return: The create method of the entity.
    """
    entity_name, entity_primary_key = get_utility_resources(entity)
    return f"""
    def create_{entity_name.lower()}(self, {entity_name.lower()}: {entity_name}) -> dict:
        return self.put_item('{entity['table']}', remove_null_values({{
            {generate_pk_sk_put(entity_primary_key, table_configuration, entity_name)},   
{generate_fields(entity, entity_name)}
        }}))
    """


def __generate_delete_method(entity: dict, table_configuration: dict) -> str:
    """
    This method generates the delete method of the entity.
    :param entity: The entity.
    :param table_configuration: The configuration of the table.
    :return: The delete method of the entity.
    """
    entity_name, entity_primary_key = get_utility_resources(entity)
    return f"""
    def delete_{entity_name.lower()}(self, {entity_primary_key[0]}) -> dict:
        item_keys = {{
            {generate_pk_sk(entity_primary_key, table_configuration, entity_name)}
        }}
        self.remove_associated_link('{entity['table']}', '{table_configuration['GSI']['index_name']}', item_keys)
        return self.delete_item('{entity['table']}', item_keys)
    """


def __generate_update_method(entity: dict, table_configuration: dict, api: dict) -> str:
    """
    This method generates the update method of the entity.
    :param entity: The entity.
    :param table_configuration: The configuration of the table.
    :param api: The API.
    :return: The update method of the entity.
    """
    entity_name, entity_primary_key = get_utility_resources(entity)
    return f"""
    def update_{entity_name.lower()}(self, arguments: dict) -> dict:
        return self.update_item('{entity['table']}', {{
            {generate_pk_sk_update(entity_primary_key, table_configuration, entity_name)}
        }}, {{
{generate_arguments_update(api['parameters'])}
        }})
    """


def __generate_get_entity_method(entity: dict, table_configuration: dict) -> str:
    """
    This method generates the get method of the entity.
    :param entity: The entity.
    :param table_configuration: The configuration of the table.
    :return: The get method of the entity.
    """
    entity_name, entity_primary_key = get_utility_resources(entity)
    return f"""
    def get_{entity_name.lower()}(self, {entity_primary_key[0]}) -> dict:
        return self.get_item('{entity['table']}', {{
            {generate_pk_sk(entity_primary_key, table_configuration, entity_name)}
        }})
    """


def __generate_get_entities_method(entity: dict, table_configuration: dict) -> str:
    """
    This method generates the get all method of the entity.
    :param entity: The entity.
    :param table_configuration: The configuration of the table.
    :return: The get all method of the entity.
    """
    entity_name, entity_primary_key = get_utility_resources(entity)
    return f"""
    def get_all_{entity_name.lower()}(self) -> list:
        query = Key('{table_configuration['sort_key']['name']}').eq('{table_configuration['parameters']['single_entity_storage_keyword']}') & Key('{table_configuration['partition_key']['name']}').begins_with('{entity_name}')
        items = self.get_items('{entity['table']}', query, index='{table_configuration['GSI']['index_name']}')
        return list(map(lambda item: self.get_{entity_name.lower()}(item['{table_configuration['partition_key']['name']}'].split('{table_configuration['parameters']['id_separator']}')[1]), items))
    """
