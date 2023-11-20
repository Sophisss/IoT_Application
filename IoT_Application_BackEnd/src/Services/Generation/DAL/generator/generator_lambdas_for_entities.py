from generator_header import generator_header_api
from generator_lambda_entity import generator_lambda


def generator_api_for_entities(json):
    result = [generator_header_api(json)]
    for entity in json['entities']:
        result.append(generator_lambda(entity, json['links']))
        result.append(generator_exception_handling())
    return ''.join(result)


def generator_exception_handling():
    return f"""
    except (IdAlreadyExistsError, ItemNotPresentError, EntitiesNotPresentError) as err:
        return {{'errors': {{'message': err.message,
                           'type': err.type}}
                }}
    else:
        return response
"""
