"""This file is responsible for generating the queries and mutations in the schema.graphql file."""
from services.generation.graphql_resources.schema.generate_parameters import generate_parameters_entity, \
    generate_parameters_link
from services.generation.graphql_resources.schema.generate_types_schema import search_types_primary_key_field


def generate_queries_mutations(entities, links):
    queries_entities, mutation_entities = zip(*map(generate_queries_mutations_entity, entities))
    queries_links, mutation_links = zip(*map(lambda link: generate_queries_mutations_link(link, entities), links))

    return ''.join(queries_entities + queries_links), ''.join(mutation_entities + mutation_links)


def generate_queries_mutations_entity(entity):
    return (
        ''.join(map(lambda
                        api: f"""\n  {api['name']}(\n   {generate_parameters_entity(entity, api)}\n  ): {entity["name"]}\n""",
                    filter(lambda api: api['type'] in ['GET'], entity['API']))) +
        ''.join(map(lambda
                        api: f"""\n  {api['name']}: {f'[{entity["name"]}]'}\n""",
                    filter(lambda api: api['type'] in ['GET_ALL'], entity['API']))),
        ''.join(map(lambda
                        api: f"\n  {api['name']}(\n   {generate_parameters_entity(entity, api)}\n  ): {'String' if api['type'] == 'PUT' else entity['name']}\n",
                    filter(lambda api: api['type'] in ['POST', 'DELETE', 'PUT'], entity['API'])))
    )


def generate_queries_mutations_link(link, entities):
    type_partition_key, type_sort_key = search_types_primary_key_field(entities, link)
    return (
        ''.join(map(lambda
                        api: f"""\n  {api['name']}(\n   {generate_parameters_link(link, api, type_partition_key, type_sort_key)}): {f'{link["first_entity"]}{link["second_entity"]}'}\n""",
                    filter(lambda api: api['type'] in ['GET'], link['API']))),
        ''.join(map(lambda
                        api: f"""\n  {api['name']}(\n   {generate_parameters_link(link, api, type_partition_key, type_sort_key)}\n  ): {'String'
        if api['type'] == 'PUT' else f'{link["first_entity"]}{link["second_entity"]}'}\n""",
                    filter(lambda api: api['type'] in ['POST', 'DELETE', 'PUT'], link['API'])))
    )
