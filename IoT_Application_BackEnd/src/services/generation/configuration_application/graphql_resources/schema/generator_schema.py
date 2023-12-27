from services.generation.configuration_application.graphql_resources.schema.resources.generator_input import generate_inputs
from services.generation.configuration_application.graphql_resources.schema.resources.generator_query_mutation import \
    generate_queries_mutations
from services.generation.configuration_application.graphql_resources.schema.resources.generator_types_schema import generate_types


def generate_graphql_schema(json: dict) -> str:
    """
    This function generates the GraphQL schema from the JSON file.
    :param json: the JSON file.
    :return: the GraphQL schema.
    """
    types = generate_types(json['entities'], json['links'])
    queries, mutation = generate_queries_mutations(json['entities'], json['links'])
    input_types = generate_inputs(json['entities'], json['links'])
    return f"""
{types}
type Query {{
{queries}
}}

type Mutation {{
{mutation}
}}

{input_types}
"""
