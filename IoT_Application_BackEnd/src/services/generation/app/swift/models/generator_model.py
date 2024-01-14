from services.generation.attribute_type import AttributeType
from services.generation.utility_methods import generate_resource_name
from services.generation.configuration_application.dal_resources.model.generator_model_link import \
    __search_primary_key_field
from services.generation.utility_methods import get_links_associated


def generate_model(item: dict, json: dict) -> str:
    return f"""import Foundation

{__generate_class(item, json)}
        """


def __generate_class(item: dict, json: dict) -> str:
    name = generate_resource_name(item)
    link_associated_first_entity, link_associated_second_entity = None, None
    if item.get("first_entity"):
        fields = [*__search_primary_key_field(json["entities"], item)] + item["fields"]
    else:
        fields = item["fields"]
        link_associated_first_entity, link_associated_second_entity = get_links_associated(item, json["links"])
    return f"""struct {name}: Codable {{
{__generate_fields(fields, link_associated_first_entity, link_associated_second_entity)}

    enum CodingKeys: String, CodingKey {{
{__generate_coding_keys(name, fields) if link_associated_first_entity is None  
        else __generate_coding_keys(name, fields, link_associated_first_entity + link_associated_second_entity)}
  }}
}}
    """


def __generate_fields(fields: dict, link_associated_first_entity, link_associated_second_entity) -> str:
    """
    This method generate the fields for a model.
    :param fields: The fields to generate.
    :return: The fields generated.
    """
    to_return = "\n".join(__create_field(field) for field in fields)
    if (link_associated_first_entity and link_associated_second_entity) is not None:
        to_return += __generate_fields_links(link_associated_first_entity, link_associated_second_entity)
    return to_return


def __generate_fields_links(links_associated_first_entity, links_associated_second_entity) -> str:
    to_return = "\n"
    for link in links_associated_first_entity:
        to_return += f"""    var {link['second_entity']}: [{link['second_entity']}]?\n""" if link["numerosity"] in [
            "one-to-many", "many-to-many"] else f"""    var {link['second_entity']}: {link['second_entity']}?\n"""
    for link in links_associated_second_entity:
        to_return += f"""    var {link['first_entity']}: [{link['first_entity']}]?\n""" if link["numerosity"] in [
            "many-to-one", "many-to-many"] else f"""    var {link['first_entity']}: {link['first_entity']}?\n"""
    return to_return


def __create_field(field: dict) -> str:
    """
    This method creates a field for a model.
    :param field: The field to create.
    :return: The field created.
    """
    is_required = field["required"]
    field_name = field["name"]
    field_type = AttributeType[field["type"]].value
    return f"""    var {field_name}: {field_type}{'?' if not is_required else ''}"""


def __generate_coding_keys(item_name, fields: dict, links=None) -> str:
    """
    This method generate the CodingKeys for a model.
    :param fields: The fields to generate.
    :return: The CodingKeys generated.
    """
    if links:
        fields = [field['name'] for field in fields] + [
            item['first_entity'] if item_name == item['second_entity'] else item['second_entity'] for item in links]
        return "\n".join(__create_coding_keys(field) for field in fields)
    else:
        return "\n".join(__create_coding_keys(field['name']) for field in fields)


def __create_coding_keys(field: str) -> str:
    """
    This method creates a CodingKeys for a model.
    :param field: The field to create.
    :return: The CodingKeys created.
    """

    return f"""        case {field} = \"{field}\""""
