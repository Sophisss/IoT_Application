from Services.Generation.DAL.generator.generator_header import generator_header_api
from Services.Generation.DAL.generator.generator_lambda_entity import generator_lambda


def generator_api_for_entities(json):
    """
    This function generates the api for the entities.
    :param json: The json with the entities.
    :return: The api for the entities.
    """
    result = [generator_header_api(json)]
    for entity in json['entities']:
        result.append(generator_lambda(entity, json['links']))
        result.append(generator_exception_handling())
    return ''.join(result)


def generator_exception_handling():
    """
    This function generates the exception handling.
    :return: The exception handling.
    """
    return """
    except (IdAlreadyExistsError, ItemNotPresentError, EntitiesNotPresentError) as err:
        return {'errors': {'message': err.message,
                           'type': err.type}
                }
    else:
        return response
"""