from services.generation.configuration_application.dal_resources.dynamo_manager.project_dynamo_manager.resources.utility_methods import get_utility_resources, generate_pk_sk_put, generate_fields, generate_pk_sk, \
    generate_pk_sk_update, generate_arguments_update, get_entities_name
from services.generation.utility_methods import get_table_configuration


def generate_link_methods(link: dict, json_data: dict) -> str:
    """
    This method generates the methods of the link.
    :param link: The link.
    :param json_data: The JSON schema containing information.
    :return: The methods of the link.
    """
    table_configuration = get_table_configuration(link['table'], json_data)
    return "".join(map(lambda api: __generate_link_api_method(link, api, table_configuration), link['API']))


def __generate_link_api_method(link: dict, api: dict, table_configuration: dict) -> str:
    """
    This method generates the methods of the link.
    :param link: The link.
    :param api: The API.
    :param table_configuration: The configuration of the table.
    :return: The methods of the link.
    """
    methods_to_return = ""
    match api['type']:
        case 'GET':
            methods_to_return += __generate_get_link_method(link, table_configuration)
        case 'POST':
            methods_to_return += __generate_update_method(link, table_configuration, api)
        case 'PUT':
            methods_to_return += __generate_create_method(link, table_configuration)
        case 'DELETE':
            methods_to_return += __generate_delete_method(link, table_configuration)
    return methods_to_return


def __generate_create_method(link: dict, table_configuration: dict) -> str:
    """
    This method generates the create method of the link.
    :param link: The link.
    :param table_configuration: The configuration of the table.
    :return: The create method of the link.
    """
    link_name, link_primary_key = get_utility_resources(link)
    first_entity, second_entity = get_entities_name(link)
    method_name = f"{first_entity.lower()}_{second_entity.lower()}"
    return f"""
    def create_{method_name}(self, link: {link_name}) -> dict:
        if self.get_{first_entity.lower()}(link.{link_primary_key[0]}) is None or self.get_{second_entity.lower()}(link.{link_primary_key[1]}) is None:
            raise ItemNotPresentError()
        return self.put_item('{link['table']}', remove_null_values({{
            {generate_pk_sk_put(link_primary_key, table_configuration, first_entity, second_entity)},
{generate_fields(link, 'link')}
        }}))
    """


def __generate_delete_method(link: dict, table_configuration: dict) -> str:
    """
    This method generates the delete method of the link.
    :param link: The link.
    :param table_configuration: The configuration of the table.
    :return: The delete method of the link.
    """
    link_name, link_primary_key = get_utility_resources(link)
    first_entity, second_entity = get_entities_name(link)
    method_name = f"{first_entity.lower()}_{second_entity.lower()}"
    return f"""
    def delete_{method_name}(self, {link_primary_key[0]}, {link_primary_key[1]}) -> dict:
        return self.delete_item('{link['table']}', {{
            {generate_pk_sk(link_primary_key, table_configuration, first_entity, second_entity)}
        }})
    """


def __generate_update_method(link: dict, table_configuration: dict, api: dict) -> str:
    """
    This method generates the update method of the link.
    :param link: The link.
    :param table_configuration: The configuration of the table.
    :param api: The API.
    :return: The update method of the link.
    """
    link_name, link_primary_key = get_utility_resources(link)
    first_entity, second_entity = get_entities_name(link)
    method_name = f"{first_entity.lower()}_{second_entity.lower()}"
    return f"""
    def update_{method_name}(self, arguments: dict) -> dict:
        return self.update_item('{link['table']}', {{
            {generate_pk_sk_update(link_primary_key, table_configuration, first_entity, second_entity)}
        }}, remove_null_values({{
{generate_arguments_update(api['parameters'])}
        }}))
    """


def __generate_get_link_method(link: dict, table_configuration: dict) -> str:
    """
    This method generates the get method of the link.
    :param link: The link.
    :param table_configuration: The configuration of the table.
    :return: The get method of the link.
    """
    link_name, link_primary_key = get_utility_resources(link)
    first_entity, second_entity = get_entities_name(link)
    method_name = f"{first_entity.lower()}_{second_entity.lower()}"
    return f"""
    def get_{method_name}(self, {link_primary_key[0]}, {link_primary_key[1]}) -> dict:
        return self.get_item('{link['table']}', {{
            {generate_pk_sk(link_primary_key, table_configuration, first_entity, second_entity)}
        }})
    """
