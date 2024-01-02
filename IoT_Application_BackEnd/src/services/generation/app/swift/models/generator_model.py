from services.generation.attribute_type import AttributeType


def generate_model(item: dict, item_name: str) -> str:
    """
    This method generate a swift model.
    :param item: Item which generate the model.
    :param item_name: Name of the item.
    :return: The model generated.
    """
    return f"""import Foundation
    
    
    
{__generate_class(item, item_name)}
    """


def __generate_class(item: dict, item_name: str) -> str:
    """
    This method generate the class for a model.
    :param item: Item which generate the class.
    :param item_name: Name of the item.
    :return: The class generated.
    """
    return f"""struct {item_name}: Codable {{
    
{__generate_fields(item['fields'])}

    enum CodingKeys: String, CodingKey {{
{__generate_CodingKeys(item['fields'])}
    }}

{__generate_enum(item['fields'])}
}}

    """


def __generate_fields(fields: dict) -> str:
    """
    This method generate the fields for a model.
    :param fields: The fields to generate.
    :return: The fields generated.
    """
    return "\n".join(__create_field(field) for field in fields)


def __create_field(field: dict) -> str:
    """
    This method creates a field for a model.
    :param field: The field to create.
    :return: The field created.
    """
    is_required = field["required"]
    field_name = field["name"]
    field_type = AttributeType[field["type"]].value if "allowedValues" not in field else f"Allowed{field_name}"
    return f"""    var {field_name}: {field_type}{'?' if not is_required else ''}"""


def __generate_CodingKeys(fields: dict) -> str:
    """
    This method generate the CodingKeys for a model.
    :param fields: The fields to generate.
    :return: The CodingKeys generated.
    """
    return "\n".join(__create_CodingKeys(field) for field in fields)


def __create_CodingKeys(field: dict) -> str:
    """
    This method creates a CodingKeys for a model.
    :param field: The field to create.
    :return: The CodingKeys created.
    """
    field_name = field["name"]
    return f"""        case {field_name} = \"{field_name}\""""


def __generate_enum(fields: dict) -> str:
    """
    This method generates the enums for a model.
    :param fields: The fields to generate.
    :return: The enums generated.
    """
    return "\n".join(__create_enum(field) for field in fields if "allowedValues" in field)


def __create_enum(field: dict) -> str:
    """
    This method creates an enum.
    :param field: Field which generate the enum.
    :return: The enum created.
    """
    field_name = field["name"]
    field_type = AttributeType[field["type"]].value
    enum_values = '\n'.join(f"        case {value.upper()} = \"{value}\"" for value in field['allowedValues'])
    return f"""    public enum Allowed{field_name}: {field_type}, Codable {{
{enum_values}
    }}
    """
