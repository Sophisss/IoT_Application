def generate_header_model():
    return """from typing import Optional
from pydantic import Field, BaseModel
"""


def generate_model_fields(fields):
    fields_result = []
    for field in fields:
        if field["type"] == "string":
            fields_result.append(generate_field_string(field))
        elif field["type"] == "integer":
            fields_result.append(generate_field_integer(field))
        elif field["type"] == "boolean":
            fields_result.append(generate_field_boolean(field))
    return "\n    ".join(fields_result)


def generate_field_string(field):
    if field.get('minLength') is not None and field.get('maxLength') is not None:
        if field['required'] is False:
            return f"{field['name']}: Optional[str] = Field(default=None, min_length={field['minLength']}, max_length={field['maxLength']})"
        else:
            return f"{field['name']}: str = Field(min_length={field['minLength']}, max_length={field['maxLength']})"
    else:
        if field['required'] is False:
            return f"{field['name']}: Optional[str] = Field(default=None)"
        else:
            return f"{field['name']}: str = Field()"


def generate_field_integer(field):
    if field.get('minimum') is not None and field.get('maximum') is not None:
        if field['required'] is False:
            return f"{field['name']}:Optional[int] = Field(default=None, gt={field['minimum']}, lt={field['maximum']})"
        else:
            return f"{field['name']}: int = Field(gt={field['minimum']}, lt={field['maximum']})"
    else:
        if field['required'] is False:
            return f"{field['name']}: Optional[int] = Field(default=None)"
        else:
            return f"{field['name']}: int = Field()"


def generate_field_boolean(field):
    if field['required'] is False:
        return f"{field['name']}: Optional[bool] = Field(default=None)"
    else:
        return f"{field['name']}: bool = Field()"


