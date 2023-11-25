from services.generation.dal.lambda_functions.generator_lambdas_for_entities import generator_api_for_entities
from services.generation.dal.lambda_functions.generator_lambdas_for_links import generator_lambdas_for_links


def generation_one_file(json):
    """
    This function generates the DAL file for the lambda function.
    :param json: The json file.
    :return: The DAL file.
    """
    return f"""
{generator_api_for_entities(json)}
{generator_lambdas_for_links(json)}
    """
