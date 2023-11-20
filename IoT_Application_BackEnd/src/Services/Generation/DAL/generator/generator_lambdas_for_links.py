from Services.Generation.DAL.generator.generator_lambda_link import generator_lambda_link


def generator_lambdas_for_links(json):
    """
    This function generates the api for the links.
    :param json: The json with the links.
    :return: The api for the links.
    """
    result_links = []
    for link in json['links']:
        result_links.append(generator_lambda_link(link))
    result_links.append(f"""
        case _:
            response = 'error'  
    return response     
    """)
    return ''.join(result_links)


def generator_exception_handling():
    """
    This function generates the exception handling.
    :return: The exception handling.
    """
    return f"""
    except (IdAlreadyExistsError, ItemNotPresentError, EntitiesNotPresentError) as err:
        return {{'errors': {{'message': err.message,
                           'type': err.type}}
                }}
    else:
        return response
"""
