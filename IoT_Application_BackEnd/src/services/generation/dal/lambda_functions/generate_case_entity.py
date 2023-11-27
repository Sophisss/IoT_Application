def generate_case_entity(entity, link):
    entity_name = entity['name']
    partition_key = entity['primary_key'][0]

    api_mapping = {
        'PUT': lambda api: generator_case_put(entity_name, api['name']),
        'DELETE': lambda api: generator_case_delete(entity_name, api['name'], partition_key),
        'GET_ALL': lambda api: generator_case_get_all(entity_name, api['name'], partition_key),
        'GET': lambda api: generator_case_get(entity_name, api['name'], partition_key, link),
        'POST': lambda api: generator_case_post(entity_name, api['name'], partition_key),
    }

    return ''.join([api_mapping[api['type']](api) for api in entity['API']]) + default_case()


def generator_case_put(entity_name, api_name):
    return f"""
            case '{api_name}':
                response, id_entity = dynamodb_manager.create_{entity_name}({entity_name}(**event_parse.arguments['{entity_name}']))
                response = f"{entity_name} with id {{id_entity}} created" if response['ResponseMetadata'][
                                                                        'HTTPStatusCode'] == 200 else response
    """


def generator_case_delete(entity_name, api_name, partition_key):
    return f"""
            case '{api_name}':
                response = dynamodb_manager.delete_{entity_name}(event_parse.arguments['{partition_key}'])
                if not response:
                    raise ItemNotPresentError('{entity_name}')
                response['{partition_key}'] = response.pop(dynamodb_manager.get_configuration().get_pk_table())
    """


def generator_case_get_all(entity_name, api_name, partition_key):
    return f"""
            case '{api_name}':
                response = dynamodb_manager.get_items_with_secondary_index('{entity_name}')
                if not response:
                    raise EntitiesNotPresentError('{entity_name}')
                for item in response:
                    item['{partition_key}'] = item.pop(dynamodb_manager.get_configuration().get_pk_table())
    """


def generator_case_post(entity_name, api_name, partition_key):
    return f"""
            case '{api_name}':
                response = dynamodb_manager.update_{entity_name}(event_parse.arguments)
                if not response:
                    raise ItemNotPresentError('{entity_name}')
                else:
                    response['{partition_key}'] = response.pop(dynamodb_manager.get_configuration().get_pk_table())
    """


def generator_case_get(entity_name, api_name, partition_key, link):
    return f"""
            case '{api_name}':
    """


def default_case():
    return f"""
            case _:
                raise InvalidAPIError(event_parse.field)"""
