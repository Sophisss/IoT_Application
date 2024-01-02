from services.generation.configuration_application.dal_resources.model.generator_model_resources import generate_header_model, \
    generate_fields_model


def generate_model_entity(entity_name: str, entity_fields: list) -> str:
    """
    This function generates the entity model.
    :param entity_name: name of the entity.
    :param entity_fields: fields of the entity.
    :return: the entity model.
    """
    return f"""{generate_header_model()}

class {entity_name}(BaseModel):
{generate_fields_model(entity_fields)}
"""
