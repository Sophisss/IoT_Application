"""This file generates the GraphQL schema from the JSON file"""
from services.generation.configuration_application.graphql_resources.schema.generate_input import generate_inputs
from services.generation.configuration_application.graphql_resources.schema.generate_query_mutation import \
    generate_queries_mutations
from services.generation.configuration_application.graphql_resources.schema.generate_types_schema import generate_types


def generate_graphql_schema(file_json) -> str:
    types = generate_types(file_json['entities'], file_json['links'])
    queries, mutation = generate_queries_mutations(file_json['entities'], file_json['links'])
    input_types = generate_inputs(file_json['entities'], file_json['links'])
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
