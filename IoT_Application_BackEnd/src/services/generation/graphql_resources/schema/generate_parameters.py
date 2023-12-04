"""This file contains functions for generating parameters for queries and mutations."""
from services.generation.graphql_resources.schema.generate_fields_link import type_mapping


def generate_parameters_entity(entity, api):
    fields_primary_key = list(
        map(lambda field: '{}: {}!'.format(field['name'], type_mapping.get(field['type'], field['type'])),
            filter(lambda field: field['name'] in entity['primary_key'], entity['fields'])))

    return (
        '\n    '.join(fields_primary_key) if api['type'] in ['GET', 'DELETE']

        else '\n   '.join(fields_primary_key + list(map(lambda param: '{}: {}'.format(param, type_mapping.get(
            next((field['type'] for field in entity['fields'] if field['name'] == param), param))),
                                                        api['parameters']))) if api['type'] == 'POST'

        else f"{entity['name']}: {entity['name']}Input!"
    )


def generate_parameters_link(link, api, type_partition_key, type_sort_key):
    fields_primary_key = f"""{link['primary_key'][0]}: {type_mapping.get(type_partition_key)}!
   {link['primary_key'][1]}: {type_mapping.get(type_sort_key)}!
   """
    return (

        fields_primary_key if api['type'] in ['GET', 'DELETE']

        else f"{link['first_entity']}{link['second_entity']}: {link['first_entity']}{link['second_entity']}Input!"
        if api['type'] == 'PUT'

        else fields_primary_key +
             "\n   ".join(list(map(lambda param: '{}: {}'.format(param, type_mapping.get(
                 next((field['type'] for field in link['fields'] if field['name'] == param), param))),
                                   api['parameters'])))
    )
