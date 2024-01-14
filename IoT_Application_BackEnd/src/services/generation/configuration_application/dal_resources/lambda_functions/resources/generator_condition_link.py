from services.generation.utility_methods import generate_resource_name, get_links_associated


def generate_condition_link(entity, links, name_partition_key_field: str, id_separator: str):
    link_first_entity, link_second_entity = get_links_associated(entity, links)
    def_first_entity, get_first_entity, get_a_first_entity = generate_condition_get_link_first_entity(link_first_entity,
                                                                                                      name_partition_key_field,
                                                                                                      id_separator)
    def_second_entity, get_second_entity, get_a_second_entity = generate_condition_get_link_second_entity(
        link_second_entity,
        name_partition_key_field,
        id_separator)
    return def_first_entity + def_second_entity, get_first_entity + get_second_entity, get_a_first_entity + get_a_second_entity


def generate_condition_get_link_first_entity(links: list, name_partition_key_field: str, id_separator: str) -> tuple[
    str, str, str]:
    condition_get, condition_def, condition_get_all = "", "", ""
    for link in links:
        c_def, c_get, c_get_all = "", "", ""
        match link['numerosity']:
            case 'one-to-many':
                c_def, c_get, c_get_all = generate_case_one_to_many_or_many_to_many_first_entity(link,
                                                                                                 name_partition_key_field,
                                                                                                 id_separator)

            case 'many-to-one':
                c_def, c_get, c_get_all = generate_case_many_to_one_or_one_to_one_first_entity(link,
                                                                                               name_partition_key_field,
                                                                                               id_separator)

            case 'many-to-many':
                c_def, c_get, c_get_all = generate_case_one_to_many_or_many_to_many_first_entity(link,
                                                                                                 name_partition_key_field,
                                                                                                 id_separator)

            case 'one-to-one':
                c_def, c_get, c_get_all = generate_case_many_to_one_or_one_to_one_first_entity(link,
                                                                                               name_partition_key_field,
                                                                                               id_separator)

        condition_def += c_def
        condition_get += c_get
        condition_get_all += c_get_all

    return condition_def, condition_get, condition_get_all


def generate_condition_get_link_second_entity(links: list, name_partition_key_field: str, id_separator: str) -> tuple[
    str, str, str]:
    condition_get, condition_def, condition_get_all = "", "", ""

    for link in links:
        c_def, c_get, c_get_all = "", "", ""
        match link['numerosity']:
            case 'one-to-many':
                c_def, c_get, c_get_all = generate_case_one_to_many_or_one_to_one_second_entity(link,
                                                                                                name_partition_key_field,
                                                                                                id_separator)

            case 'many-to-one':
                c_def, c_get, c_get_all = generate_case_many_to_one_or_many_to_many_second_entity(link,
                                                                                                  name_partition_key_field,
                                                                                                  id_separator)

            case 'many-to-many':
                c_def, c_get, c_get_all = generate_case_one_to_many_or_one_to_one_second_entity(link,
                                                                                                name_partition_key_field,
                                                                                                id_separator)

            case 'one-to-one':
                c_def, c_get, c_get_all = generate_case_many_to_one_or_many_to_many_second_entity(link,
                                                                                                  name_partition_key_field,
                                                                                                  id_separator)
        condition_def += c_def
        condition_get += c_get
        condition_get_all += c_get_all

    return condition_def, condition_get, condition_get_all


def generate_case_many_to_one_or_one_to_one_first_entity(link: dict, name_partition_key_field: str,
                                                         id_separator: str) -> tuple[str, str, str]:
    second_entity = link['second_entity']
    first_entity = link['first_entity']
    condition_def = f"""
def __condition_get_{second_entity.lower()}({link['primary_key'][0]}, project_manager, {first_entity.lower()}):
    res = project_manager.get_{second_entity.lower()}_for_{first_entity.lower()}({link['primary_key'][0]})
    if res:
        check_response_item(res)
        check_response_status(res)
        {first_entity.lower()}['{second_entity}'] = change_name_keys(res['Item'], ('{link['primary_key'][1]}', '{name_partition_key_field}', '{id_separator}'))
    else:
        {first_entity.lower()}['{second_entity}'] = None
        """

    condition_get = f"""
                if '{second_entity}' in event_parse.projection:
                    __condition_get_{second_entity.lower()}(event_parse.arguments['{link['primary_key'][0]}'], project_manager, response)
                    """
    condition_get_all = f"""
                if '{second_entity}' in event_parse.projection:
                    for {first_entity.lower()} in response:
                        __condition_get_{second_entity.lower()}(event_parse.arguments['{link['primary_key'][0]}'], project_manager, {first_entity.lower()})
                    """
    return condition_def, condition_get, condition_get_all


def generate_case_one_to_many_or_many_to_many_first_entity(link: dict, name_partition_key_field: str,
                                                           id_separator: str) -> tuple[str, str, str]:
    second_entity = link['second_entity']
    first_entity = link['first_entity']
    condition_def = f"""
def __condition_get_{second_entity.lower()}({link['primary_key'][0]}, project_manager, {first_entity.lower()}):
    res = project_manager.get_all_{second_entity.lower()}_for_{first_entity.lower()}({link['primary_key'][0]})
    if res:
        for item in res:
            check_response_status(item)
    {first_entity.lower()}['{second_entity}'] = list(
         map(lambda {second_entity.lower()}: change_name_keys({second_entity.lower()}['Item'], ('{link['primary_key'][1]}', '{name_partition_key_field}', '{id_separator}')), res))
         """
    condition_get = f"""
                if '{second_entity}' in event_parse.projection:
                    __condition_get_{second_entity.lower()}(event_parse.arguments['{link['primary_key'][0]}'], project_manager, response)
                    """
    condition_get_all = f"""
                if '{second_entity}' in event_parse.projection:
                    for {first_entity.lower()} in response:
                        __condition_get_{second_entity.lower()}(event_parse.arguments['{link['primary_key'][0]}'], project_manager, {first_entity.lower()})
                       """
    return condition_def, condition_get, condition_get_all


def generate_case_one_to_many_or_one_to_one_second_entity(link: dict, name_partition_key_field: str,
                                                          id_separator: str) -> tuple[str, str, str]:
    second_entity = link['second_entity']
    first_entity = link['first_entity']
    condition_def = f"""
def __condition_get_{first_entity.lower()}({link['primary_key'][1]}, project_manager, {second_entity.lower()}):
    res = project_manager.get_{first_entity.lower()}_for_{second_entity.lower()}({link['primary_key'][1]})
    if res:
        check_response_item(res)
        check_response_status(res)
        {second_entity.lower()}['{first_entity}'] = change_name_keys(res['Item'], ('{link['primary_key'][0]}', '{name_partition_key_field}', '{id_separator}'))
    else:
        {second_entity.lower()}['{first_entity}'] = None
        """
    condition_get = f"""
                if '{first_entity}' in event_parse.projection:
                    __condition_get_{first_entity.lower()}(event_parse.arguments['{link['primary_key'][0]}'], project_manager, response)
                    """
    condition_get_all = f"""
                if '{first_entity}' in event_parse.projection:
                    for {second_entity.lower()} in response:
                        __condition_get_{first_entity.lower()}(event_parse.arguments['{link['primary_key'][0]}'], project_manager, {second_entity.lower()})
    """
    return condition_def, condition_get, condition_get_all


def generate_case_many_to_one_or_many_to_many_second_entity(link: dict, name_partition_key_field: str,
                                                            id_separator: str) -> tuple[str, str, str]:
    second_entity = link['second_entity']
    first_entity = link['first_entity']
    condition_def = f"""
def __condition_get_{first_entity.lower()}({link['primary_key'][1]}, project_manager, {second_entity.lower()}):
    res = project_manager.get_all_{first_entity.lower()}_for_{second_entity.lower()}({link['primary_key'][1]})
    if res:
        for item in res:
            check_response_status(item)
    {second_entity.lower()}['{first_entity}'] = list(
        map(lambda {first_entity.lower()}: change_name_keys({first_entity.lower()}['Item'], ('{link['primary_key'][0]}', '{name_partition_key_field}', '{id_separator}')), res))
        """
    condition_get = f"""
                if '{first_entity}' in event_parse.projection:
                    __condition_get_{first_entity.lower()}(event_parse.arguments['{link['primary_key'][1]}'], project_manager, response)
                    """
    condition_get_all = f"""
                if '{first_entity}' in event_parse.projection:
                    for {second_entity.lower()} in response:
                        __condition_get_{first_entity.lower()}(event_parse.arguments['{link['primary_key'][1]}'], project_manager, {second_entity.lower()})
    """
    return condition_def, condition_get, condition_get_all
