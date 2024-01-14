def generate_case_get_link_first_entity(links: list) -> str:
    to_return = ""

    for link in links:
        match link['numerosity']:
            case 'one-to-many':
                to_return += generate_case_one_to_many_or_many_to_many_first_entity(link)
            case 'many-to-one':
                to_return += generate_case_many_to_one_or_one_to_one_first_entity(link)
            case 'many-to-many':
                to_return += generate_case_one_to_many_or_many_to_many_first_entity(link)
            case 'one-to-one':
                to_return += generate_case_many_to_one_or_one_to_one_first_entity(link)

    return to_return


def generate_case_get_link_second_entity(links: list) -> str:
    to_return = ""

    for link in links:
        match link['numerosity']:
            case 'one-to-many':
                to_return += generate_case_one_to_many_or_one_to_one_second_entity(link)
            case 'many-to-one':
                to_return += generate_case_many_to_one_or_many_to_many_second_entity(link)
            case 'many-to-many':
                to_return += generate_case_one_to_many_or_one_to_one_second_entity(link)
            case 'one-to-one':
                to_return += generate_case_many_to_one_or_many_to_many_second_entity(link)

    return to_return


def generate_case_many_to_one_or_one_to_one_first_entity(link: dict) -> str:
    second_entity = link['second_entity']
    return f"""
                if '{second_entity}' in event_parse.projection:
                    __condition_get_{second_entity.lower()}(event_parse.arguments['{link['primary_key'][0]}'],project_manager, response)"""


def generate_case_one_to_many_or_many_to_many_first_entity(link: dict) -> str:
    second_entity = link['second_entity']
    return f"""
                if '{second_entity}' in event_parse.projection:
                    __condition_get_{second_entity.lower()}(event_parse.arguments['{link['primary_key'][0]}'],project_manager, response)"""


def generate_case_one_to_many_or_one_to_one_second_entity(link: dict) -> str:
    first_entity = link['first_entity']
    return f"""
                if '{first_entity}' in event_parse.projection:
                    __condition_get_{first_entity.lower()}(event_parse.arguments['{link['primary_key'][1]}'],project_manager, response)"""


def generate_case_many_to_one_or_many_to_many_second_entity(link: dict) -> str:
    first_entity = link['first_entity']
    return f"""
                if '{first_entity}' in event_parse.projection:
                    __condition_get_{first_entity.lower()}(event_parse.arguments['{link['primary_key'][1]}'],project_manager, response)"""
