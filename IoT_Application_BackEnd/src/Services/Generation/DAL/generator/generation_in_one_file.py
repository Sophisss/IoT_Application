from Services.Generation.DAL.generator.generator_lambdas_for_entities import generator_api_for_entities
from Services.Generation.DAL.generator.generator_lambdas_for_links import generator_lambdas_for_links


def generation_one_file(json):
    return f"""
{generator_api_for_entities(json)}
{generator_lambdas_for_links(json)}
    """