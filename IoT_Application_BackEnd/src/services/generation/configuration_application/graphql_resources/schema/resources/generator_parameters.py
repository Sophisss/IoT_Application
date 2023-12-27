from services.generation.configuration_application.graphql_resources.schema.resources.generator_fields_link import type_mapping


def generate_parameters_entity(entity: dict, api) -> str:
    """
    This function generates the parameters for queries and mutations for an entity.
    :param entity: entity for which the parameters are generated.
    :param api: api for which the parameters are generated.
    :return: the parameters for queries and mutations for an entity.
    """
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


def generate_parameters_link(link: dict, api, type_partition_key, type_sort_key) -> str:
    """
    This function generates the parameters for queries and mutations for a link.
    :param link: link for which the parameters are generated.
    :param api: api for which the parameters are generated.
    :param type_partition_key: type of the partition key.
    :param type_sort_key: type of the sort key.
    :return: the parameters for queries and mutations for a link.
    """
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
