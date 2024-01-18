from services.generation.configuration_application.graphql_resources.schema.resources.generator_parameters import \
    generate_parameters_entity, generate_parameters_link
from services.generation.configuration_application.graphql_resources.schema.resources.generator_types_schema import \
    search_types_primary_key_field


def generate_queries_mutations(entities: list, links: list) -> tuple:
    """
    This function generates the queries and mutations for the GraphQL schema.
    :param entities: entities for which the queries and mutations are generated.
    :param links: links for which the queries and mutations are generated.
    :return: the queries and mutations for the GraphQL schema.
    """
    queries_entities, mutation_entities = zip(
        *map(lambda entity: __generate_queries_mutations_entity(entity, links), entities))
    if bool(links):
        queries_links, mutation_links = zip(*map(lambda link: __generate_queries_mutations_link(link, entities), links))
        return ''.join(queries_entities + queries_links), ''.join(mutation_entities + mutation_links)
    else:
        return ''.join(queries_entities), ''.join(mutation_entities)


def __generate_queries_mutations_entity(entity: dict, links: list) -> tuple:
    """
    This function generates the queries and mutations for an entity.
    :param entity: entity for which the queries and mutations are generated.
    :return: the queries and mutations for an entity.
    """
    return (
        ''.join(map(lambda
                        api: f"""\n  {api['name']}(\n   {generate_parameters_entity(entity, api, links)}\n  ): {entity["name"]}\n""",
                    filter(lambda api: api['type'] in ['GET'], entity['API']))) +
        ''.join(map(lambda
                        api: f"""\n  {api['name']}: {f'[{entity["name"]}]'}\n""",
                    filter(lambda api: api['type'] in ['GET_ALL'], entity['API']))),
        ''.join(map(lambda
                        api: f"""\n  {api['name']}(\n   {generate_parameters_entity(entity, api, links)}\n  ): String  \n""",
                    filter(lambda api: api['type'] in ['POST', 'DELETE', 'PUT'], entity['API'])))
    )


def __generate_queries_mutations_link(link: dict, entities: list) -> tuple:
    """
    This function generates the queries and mutations for a link.
    :param link: link for which the queries and mutations are generated.
    :param entities: entities of the project.
    :return: the queries and mutations for a link.
    """
    type_partition_key, type_sort_key = search_types_primary_key_field(entities, link)
    return (
        ''.join(map(lambda
                        api: f"""\n  {api['name']}(\n   {generate_parameters_link(link, api, type_partition_key, type_sort_key)}): {f'{link["first_entity"]}{link["second_entity"]}'}\n""",
                    filter(lambda api: api['type'] in ['GET'], link['API']))),
        ''.join(map(lambda
                        api: f"""\n  {api['name']}(\n   {generate_parameters_link(link, api, type_partition_key, type_sort_key)}\n  ): String\n""",
                    filter(lambda api: api['type'] in ['POST', 'DELETE', 'PUT'], link['API'])))

    )
