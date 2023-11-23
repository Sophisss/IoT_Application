from Services.Generation.DAL.Model.generator_model import generate_header_model, generate_model_fields
from Services.Generation.utility_methods import generate_resource_name


def generate_model_link(link, json):
    fields_link = [search_primary_key_field(json, link['first_entity'], link['primary_key'][0]),
                   search_primary_key_field(json, link['second_entity'], link['primary_key'][1])] + list(link['fields'])
    return f"""{generate_header_model()}
class {generate_resource_name(link)}(BaseModel):
    {generate_model_fields(fields_link)}
"""


def search_primary_key_field(json, name_entity, name_primary_key_field):
    entity_search = next(filter(lambda entity: entity['name'] == name_entity, json['entities']), None)
    field_primary_key = next(filter(lambda field: field['name'] == name_primary_key_field, entity_search['fields']),
                             None) if entity_search else None
    return field_primary_key
