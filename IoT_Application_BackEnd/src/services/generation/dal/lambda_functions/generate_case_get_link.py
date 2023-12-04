def generate_case_get_link_first_entity(links, name_partition_key_field):
    mapping = {
        'one-to-many': generate_case_one_to_many_or_many_to_many_first_entity,
        'many-to-one': generate_case_many_to_one_or_one_to_one_first_entity,
        'many-to-many': generate_case_one_to_many_or_many_to_many_first_entity,
        'one-to-one': generate_case_many_to_one_or_one_to_one_first_entity
    }

    return ''.join([mapping[link['numerosity']](link, name_partition_key_field) for link in links])


def generate_case_get_link_second_entity(links, name_partition_key_field):
    mapping = {
        'one-to-many': generate_case_one_to_many_or_one_to_one_second_entity,
        'many-to-one': generate_case_many_to_one_or_many_to_many_second_entity,
        'many-to-many': generate_case_many_to_one_or_many_to_many_second_entity,
        'one-to-one': generate_case_one_to_many_or_one_to_one_second_entity
    }

    return ''.join([mapping[link['numerosity']](link, name_partition_key_field) for link in links])


def generate_case_many_to_one_or_one_to_one_first_entity(link, name_partition_key_field):
    second_entity = link['second_entity']
    first_entity = link['first_entity']
    return f"""
                 if '{second_entity}' in event_parse.projection:
                    res = project_manager.get_{second_entity.lower()}_for_{first_entity.lower()}(event_parse.arguments['{link['primary_key'][0]}'])
                    response['{second_entity}'] = change_name_keys(res['Item'], ('{link['primary_key'][1]}', '{name_partition_key_field}'))              """


def generate_case_one_to_many_or_many_to_many_first_entity(link, name_partition_key_field):
    second_entity = link['second_entity']
    first_entity = link['first_entity']
    return f"""
                if '{second_entity}' in event_parse.projection:
                    res = project_manager.get_all_{second_entity.lower()}_for_{first_entity.lower()}(event_parse.arguments['{link['primary_key'][0]}'])
                    response['{second_entity}'] = list(
                        map(lambda {second_entity.lower()}: change_name_keys({second_entity.lower()}['Item'], ('{link['primary_key'][1]}', '{name_partition_key_field}')), res))"""


def generate_case_one_to_many_or_one_to_one_second_entity(link, name_partition_key_field):
    second_entity = link['second_entity']
    first_entity = link['first_entity']
    return f"""
                if '{first_entity}' in event_parse.projection:
                    res = project_manager.get_{first_entity.lower()}_for_{second_entity.lower()}(event_parse.arguments['{link['primary_key'][1]}'])
                    response['{first_entity}'] = change_name_keys(res['Item'], ('{link['primary_key'][0]}', '{name_partition_key_field}'))"""


def generate_case_many_to_one_or_many_to_many_second_entity(link, name_partition_key_field):
    second_entity = link['second_entity']
    first_entity = link['first_entity']
    return f"""
                if '{first_entity}' in event_parse.projection:
                    res = project_manager.get_all_{first_entity.lower()}_for_{second_entity.lower()}(event_parse.arguments['{link['primary_key'][1]}'])
                    response['{first_entity}'] = list(
                        map(lambda {first_entity.lower()}: change_name_keys({first_entity.lower()}['Item'], ('{link['primary_key'][0]}', '{name_partition_key_field}')), res))"""
