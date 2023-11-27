from services.generation.utility_methods import generate_resource_name


def generate_kotlin_model(item: dict) -> str:
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
    pass
