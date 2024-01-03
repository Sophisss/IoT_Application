from services.generation.attribute_type import AttributeType
from services.generation.utility_methods import get_links_associated, generate_resource_name


def generate_parameters_entity(entity: dict, api, links: list) -> str:
    """
    This function generates the parameters for queries and mutations for an entity.
    :param entity: entity for which the parameters are generated.
    :param api: api for which the parameters are generated.
    :param links: links for which the parameters are generated.
    :return: the parameters for queries and mutations for an entity.
    """
    fields_primary_key = list(
        map(lambda field: '{}: {}!'.format(field['name'], AttributeType[field['type']].value,
                                           AttributeType[field['type']].value),
            filter(lambda field: field['name'] in entity['primary_key'], entity['fields'])))

    association_link_first, association_link_second = get_links_associated(entity, links)
    links_put = ""
    for link in association_link_first and association_link_second:
        resource = generate_resource_name(link)
        links_put += f"{resource}: {resource}Input!"

    return (
        '\n    '.join(fields_primary_key) if api['type'] in ['GET', 'DELETE']

        else '\n   '.join(fields_primary_key + list(map(lambda param: '{}: {}'.format(param, AttributeType[
            next((field['type'] for field in entity['fields'] if field['name'] == param), param)].value),
                                                        api['parameters']))) if api['type'] == 'POST'

        else f"""{entity['name']}: {entity['name']}Input!
                 {links_put}"""
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
    fields_primary_key = f"""{link['primary_key'][0]}: {AttributeType[type_partition_key].value}!
   {link['primary_key'][1]}: {AttributeType[type_sort_key].value}!
   """
    return (

        fields_primary_key if api['type'] in ['GET', 'DELETE']

        else f"{link['first_entity']}{link['second_entity']}: {link['first_entity']}{link['second_entity']}Input!"
        if api['type'] == 'PUT'

        else fields_primary_key +
             "\n   ".join(list(map(lambda param: '{}: {}'.format(param, AttributeType[
                 next((field['type'] for field in link['fields'] if field['name'] == param), param)].value),
                                   api['parameters'])))
    )
