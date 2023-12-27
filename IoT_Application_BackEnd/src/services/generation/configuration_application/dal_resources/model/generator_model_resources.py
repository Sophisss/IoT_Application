def generate_header_model() -> str:
    """
    This function generates the header of the model.
    :return: the header of the model.
    """
    return """from typing import Optional
from pydantic import Field, BaseModel
"""


def generate_fields_model(fields: list) -> str:
    """
    This function generates the fields of the model.
    :param fields: the fields.
    :return: the fields generated.
    """
    return '    '.join(map(lambda field: functions_generate_fields[field['type']](field), fields))


def generate_field_model_string(field: dict) -> str:
    """
    This function generates the field if it is a string.
    :param field: the field.
    :return: the field generated.
    """

    def min_length_option():
        return f"min_length={field['minLength']}" if 'minLength' in field else ''

    def max_length_option():
        return f"max_length={field['maxLength']}" if 'maxLength' in field else ''

    options = ', '.join(filter(None, [min_length_option(), max_length_option()]))
    return (f"{field['name']}: str = Field({options})\n" if field['required']
            else f"{field['name']}: Optional[str] = Field(default=None{', '.join([min_length_option(), max_length_option()])})\n")


def generate_field_model_integer(field: dict) -> str:
    """
    This function generates the field if it is an integer.
    :param field: the field.
    :return: the field generated.
    """

    def min_option() -> str:
        return f"ge={field['minimum']}" if 'minimum' in field else ''

    def max_option() -> str:
        return f"le={field['maximum']}" if 'maximum' in field else ''

    options = ', '.join(filter(None, [min_option(), max_option()]))
    return (f"{field['name']}: int = Field({options})\n" if field['required']
            else f"{field['name']}:Optional[int] = Field(default=None{', '.join([min_option(), max_option()])})\n")


def generate_field_model_boolean(field: dict) -> str:
    """
    This function generates the field if it is a boolean.
    :param field: the field.
    :return: the field generated.
    """
    return (f"{field['name']}: bool = Field()" if field['required']
            else f"{field['name']}: Optional[bool] = Field(default=None)\n")


functions_generate_fields = {
    'string': generate_field_model_string,
    'integer': generate_field_model_integer,
    'boolean': generate_field_model_boolean,
}
