from services.generation.utility_methods import generate_resource_name


def generate_model(item: dict) -> str:
    return f"""package model
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable


{__generate_class(item)}
    """


def __generate_class(item: dict) -> str:
    return f"""@Serializable
data class {generate_resource_name(item)}(
{__generate_fields(item['fields'])}
)
    """


def __generate_fields(fields: dict) -> str:
    return "".join(map(lambda field: __create_field(field), fields))


def __create_field(field: dict) -> str:
    return f"""@SerialName("{field['name']}") val {field['name']}: {field['type']}"""
