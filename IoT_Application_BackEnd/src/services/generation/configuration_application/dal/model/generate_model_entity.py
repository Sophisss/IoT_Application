"""This file is responsible for generating the entity pydantic model."""
from services.generation.configuration_application.dal.model.generate_model import generate_header_model, \
    generate_fields_model


def generate_model_entity(name_entity: str, fields: list) -> str:
    return f"""{generate_header_model()}

class {name_entity}(BaseModel):
    {generate_fields_model(fields)}
"""
