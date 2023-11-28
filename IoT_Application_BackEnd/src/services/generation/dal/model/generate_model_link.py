"This file is responsible for generating the link pydantic model."
from generate_model import generate_header_model, generate_fields_model


def generate_model_link(link: dict, json: dict) -> str:
    link_fields = [*search_primary_key_field(json['entities'], link)]
    link_fields.extend([*link['fields']])
    return f"""{generate_header_model()}

class {link['first_entity']}{link['second_entity']}(BaseModel):
    {generate_fields_model(link_fields)}
"""


def search_primary_key_field(entities: list, link: dict) -> tuple:
    partition_key = next(filter(lambda entity: entity['name'] == link['first_entity'], entities), None)
    partition_key_field = next(
        filter(lambda field: field['name'] == link['primary_key'][0], partition_key['fields']), None)
    sort_key = next(filter(lambda entity: entity['name'] == link['second_entity'], entities), None)
    sort_key_field = next(filter(lambda field: field['name'] == link['primary_key'][1], sort_key['fields']),
                          None)
    return partition_key_field, sort_key_field
