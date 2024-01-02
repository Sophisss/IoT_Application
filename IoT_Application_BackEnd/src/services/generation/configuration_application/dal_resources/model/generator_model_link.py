from services.generation.configuration_application.dal_resources.model.generator_model_resources import generate_header_model, \
    generate_fields_model


def generate_model_link(link: dict, json: dict) -> str:
    """
    This function generates the link model.
    :param link: link for which the model is generated.
    :param json: the JSON data.
    :return: the link model.
    """
    link_fields = [*__search_primary_key_field(json['entities'], link)]
    link_fields.extend([*link['fields']])
    return f"""{generate_header_model()}

class {link['first_entity']}{link['second_entity']}(BaseModel):
{generate_fields_model(link_fields)}
"""


def __search_primary_key_field(entities: list, link: dict) -> tuple:
    """
    This function searches the partition key and sort key of the link.
    :param entities: entities of the link.
    :param link: link for which the partition key and sort key are searched.
    :return: the partition key and sort key of the link.
    """
    partition_key = next(filter(lambda entity: entity['name'] == link['first_entity'], entities), None)
    partition_key_field = next(
        filter(lambda field: field['name'] == link['primary_key'][0], partition_key['fields']), None)
    sort_key = next(filter(lambda entity: entity['name'] == link['second_entity'], entities), None)
    sort_key_field = next(filter(lambda field: field['name'] == link['primary_key'][1], sort_key['fields']),
                          None)
    return partition_key_field, sort_key_field
