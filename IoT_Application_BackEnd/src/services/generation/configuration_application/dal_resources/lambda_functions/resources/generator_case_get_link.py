def generate_case_get_link_first_entity(links: list, name_partition_key_field: str, id_separator: str) -> str:
    toReturn = ""

    for link in links:
        match link['numerosity']:
            case 'one-to-many':
                toReturn += generate_case_one_to_many_or_many_to_many_first_entity(link, name_partition_key_field,
                                                                                   id_separator)
            case 'many-to-one':
                toReturn += generate_case_many_to_one_or_one_to_one_first_entity(link, name_partition_key_field,
                                                                                 id_separator)
            case 'many-to-many':
                toReturn += generate_case_one_to_many_or_many_to_many_first_entity(link, name_partition_key_field,
                                                                                   id_separator)
            case 'one-to-one':
                toReturn += generate_case_many_to_one_or_one_to_one_first_entity(link, name_partition_key_field,
                                                                                 id_separator)

    return toReturn


def generate_case_get_link_second_entity(links: list, name_partition_key_field: str, id_separator: str) -> str:
    toReturn = ""

    for link in links:
        match link['numerosity']:
            case 'one-to-many':
                toReturn += generate_case_one_to_many_or_one_to_one_second_entity(link, name_partition_key_field,
                                                                                  id_separator)
            case 'many-to-one':
                toReturn += generate_case_many_to_one_or_many_to_many_second_entity(link, name_partition_key_field,
                                                                                    id_separator)
            case 'many-to-many':
                toReturn += generate_case_one_to_many_or_one_to_one_second_entity(link, name_partition_key_field,
                                                                                  id_separator)
            case 'one-to-one':
                toReturn += generate_case_many_to_one_or_many_to_many_second_entity(link, name_partition_key_field,
                                                                                    id_separator)

    return toReturn


def generate_case_many_to_one_or_one_to_one_first_entity(link: dict, name_partition_key_field: str,
                                                         id_separator: str) -> str:
    second_entity = link['second_entity']
    first_entity = link['first_entity']
    return f"""
                if '{second_entity}' in event_parse.projection:
                    res = project_manager.get_{second_entity.lower()}_for_{first_entity.lower()}(event_parse.arguments['{link['primary_key'][0]}'])
                    if res:
                        check_response_item(res)
                        check_response_status(res)
                        response['{second_entity}'] = change_name_keys(res['Item'], ('{link['primary_key'][1]}', '{name_partition_key_field}', '{id_separator}'))
                    else:
                        response['{second_entity}'] = None"""


def generate_case_one_to_many_or_many_to_many_first_entity(link: dict, name_partition_key_field: str,
                                                           id_separator: str) -> str:
    second_entity = link['second_entity']
    first_entity = link['first_entity']
    return f"""
                if '{second_entity}' in event_parse.projection:
                    res = project_manager.get_all_{second_entity.lower()}_for_{first_entity.lower()}(event_parse.arguments['{link['primary_key'][0]}'])
                    if res:
                        for item in res:
                            check_response_status(item)
                    response['{second_entity}'] = list(
                        map(lambda {second_entity.lower()}: change_name_keys({second_entity.lower()}['Item'], ('{link['primary_key'][1]}', '{name_partition_key_field}', '{id_separator}')), res))"""


def generate_case_one_to_many_or_one_to_one_second_entity(link: dict, name_partition_key_field: str,
                                                          id_separator: str) -> str:
    second_entity = link['second_entity']
    first_entity = link['first_entity']
    return f"""
                if '{first_entity}' in event_parse.projection:
                    res = project_manager.get_{first_entity.lower()}_for_{second_entity.lower()}(event_parse.arguments['{link['primary_key'][1]}'])
                    if res:
                        check_response_item(res)
                        check_response_status(res)
                        response['{first_entity}'] = change_name_keys(res['Item'], ('{link['primary_key'][0]}', '{name_partition_key_field}', '{id_separator}'))
                    else:
                        response['{first_entity}'] = None"""


def generate_case_many_to_one_or_many_to_many_second_entity(link: dict, name_partition_key_field: str,
                                                            id_separator: str) -> str:
    second_entity = link['second_entity']
    first_entity = link['first_entity']
    return f"""
                if '{first_entity}' in event_parse.projection:
                    res = project_manager.get_all_{first_entity.lower()}_for_{second_entity.lower()}(event_parse.arguments['{link['primary_key'][1]}'])
                    if res:
                        for item in res:
                            check_response_status(item)
                    response['{first_entity}'] = list(
                        map(lambda {first_entity.lower()}: change_name_keys({first_entity.lower()}['Item'], ('{link['primary_key'][0]}', '{name_partition_key_field}', '{id_separator}')), res))"""
