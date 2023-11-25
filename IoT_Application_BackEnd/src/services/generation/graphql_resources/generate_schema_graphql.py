type_mapping = {
    'string': 'String',
    'integer': 'Int',
}


def generate_graphql_schema(file_json) -> str:
    types = generate_types(file_json['entities'], file_json['links'])
    queries, mutation = generate_query_mutation(file_json['entities'], file_json['links'])
    input_types = generate_input(file_json['entities'])
    return f'\n{types}\n\ntype Query {{\n{queries}\n}}\n\ntype Mutation {{\n{mutation}\n}}\n\n{input_types}\n'


def generate_types(json_entities, links) -> str:
    type_codes = []
    for entity in json_entities:
        boolean_value, list_link = check_if_entity_has_link(entity, links)
        if boolean_value:
            type_codes.append(generate_type_for_entity_with_link(entity, list_link))
        else:
            type_codes.append(generate_type_for_entity_without_links(entity))
    return ''.join(type_codes)


def generate_input(json_entities):
    input_code = []
    for entity in json_entities:
        input_code.append(f'\ninput {entity["name"]}Input{{\n{generate_fields_for_entity(entity)}\n}}')
    return ''.join(input_code)


def generate_type_for_entity_with_link(entity, list_link):
    fields_code = generate_fields_for_entity(entity)
    fields_link = generate_link_fields_for_entity(entity, list_link)
    fields_code = fields_code + fields_link
    enum_code = generate_enum_for_entity(entity)
    return """\ntype {name} {{\n{fields}}}\n{enums}""".format(name=entity['name'],
                                                              fields=fields_code,
                                                              enums=enum_code)


def generate_type_for_entity_without_links(entity) -> str:
    fields_code = generate_fields_for_entity(entity)
    enum_code = generate_enum_for_entity(entity)
    return """\ntype {name} {{\n{fields}}}\n{enums}""".format(name=entity['name'],
                                                              fields=fields_code,
                                                              enums=enum_code)


def generate_fields_for_entity(entity) -> str:
    return ''.join(
        ["""{name}: {type}{required}\n""".format(name=field['name'], type=type_mapping.get(field['type'], field[
            'type']) if 'allowedValues' not in field else f"Allowed{field['name']}",
                                                 required='!' if field['required'] else '') for field in
         entity['fields']])


# QUI .lower()
def generate_link_fields_for_entity(entity, list_link) -> str:
    link_fields = []
    for link in list_link:
        if entity['name'] == link['first_entity'] and link['numerosity'] == 'one-to-many':
            link_fields.append('{name}:[{name_type}]\n'.format(name=link['second_entity'],
                                                               name_type=link['second_entity']))
        elif entity['name'] == link['first_entity'] and link['numerosity'] == 'many-to-one':
            link_fields.append('{name}:{name_type}\n'.format(name=link['second_entity'],
                                                             name_type=link['second_entity']))
        elif entity['name'] == link['second_entity'] and link['numerosity'] == 'one-to-many':
            link_fields.append('{name}:{name_type}\n'.format(name=link['first_entity'],
                                                             name_type=link['first_entity']))
        elif entity['name'] == link['second_entity'] and link['numerosity'] == 'many-to-one':
            link_fields.append('{name}:[{name_type}]\n'.format(name=link['first_entity'],
                                                               name_type=link['first_entity']))
        elif link['numerosity'] == 'many-to-many' and entity['name'] == link['first_entity']:
            link_fields.append('{name}:[{name_type}]\n'.format(name=link['second_entity'],
                                                               name_type=link['second_entity']))
        elif link['numerosity'] == 'many-to-many' and entity['name'] == link['second_entity']:
            link_fields.append('{name}:[{name_type}]\n'.format(name=link['first_entity'],
                                                               name_type=link['first_entity']))
        elif link['numerosity'] == 'one-to-one' and entity['name'] == link['first_entity']:
            link_fields.append('{name}:{name_type}\n'.format(name=link['second_entity'],
                                                             name_type=link['second_entity']))
        else:
            link_fields.append('{name}:{name_type}\n'.format(name=link['first_entity'],
                                                             name_type=link['first_entity']))
    return ''.join(link_fields)


def generate_enum_for_entity(entity):
    return ''.join(["""\nenum Allowed{name}{{\n{fields}\n}}\n""".format(name=field['name'],
                                                                        fields=generate_fields_for_enum_entity(field)
                                                                        ) for field in entity['fields'] if
                    'allowedValues' in field])


def generate_fields_for_enum_entity(entity_field) -> str:
    fields_enum = []
    for value in entity_field.get('allowedValues', []):
        fields_enum.append(f'  {value}')
    return '\n'.join(fields_enum)


def check_if_entity_has_link(entity, links) -> (bool, list):
    links_list = []
    for link in links:
        if entity['name'] in [link['first_entity'], link['second_entity']]:
            links_list.append(link)
    return bool(links_list), links_list


def generate_query_mutation(entities, links):
    queries = []
    mutation = []
    for entity in entities:
        queries_entities, mutation_entities = generate_q_m_entity(entity)
        queries.append(queries_entities)
        mutation.append(mutation_entities)
    for link in links:
        queries_link, mutation_link = generate_q_m_link(link)
        queries.append(queries_link)
        mutation.append(mutation_link)

    return ''.join(queries), ''.join(mutation)


def generate_q_m_link(link):
    queries_link = []
    mutations_link = []
    for api in link['API']:
        parameters = generate_parameters_queries_link(api, link)
        if api['type'] == 'PUT':
            operation_code = """\n  {name}(\n   {parameters}\n  ): {returns}\n""".format(name=api['name'],
                                                                                         parameters=parameters,
                                                                                         returns='String')
        else:
            operation_code = """\n  {name}(\n   {parameters}\n  ): {returns}\n""".format(name=api['name'],
                                                                                         parameters=parameters,
                                                                                         returns='[String]')
        if api['type'] == 'GET':
            if parameters.strip():
                queries_link.append(operation_code)
        elif api['type'] in ['POST', 'DELETE', 'PUT']:
            if parameters.strip():
                mutations_link.append(operation_code)
    return ''.join(queries_link), ''.join(mutations_link)


def generate_parameters_queries_link(api, link):
    parameters = ',\n   '.join(
        ['{}: String!'.format(pr) for pr in link['primary_key']])
    if api['type'] in ['PUT', 'POST']:
        parameters += ',\n   ' + parameters.join(
            ['{}:{}{required}'.format(field['name'], type_mapping.get(field['type'], field['type']),
                                      required='!' if field['required'] is True else '')
             for field in link['fields']])
    return parameters


def generate_q_m_entity(entity):
    queries_entities = []
    mutations_entities = []
    for api in entity['API']:
        parameters = generate_parameters(entity, api)
        if api['type'] == 'PUT':
            operation_code = """\n  {name}(\n   {parameters}\n  ): {returns}\n""".format(name=api['name'],
                                                                                         parameters=parameters,
                                                                                         returns='String')
        elif api['type'] == 'GET_ALL':
            operation_code = """\n  {name}: {returns}\n""".format(name=api["name"], returns=f"[{entity['name']}]")
        else:
            operation_code = """\n  {name}(\n   {parameters}\n  ): {returns}\n""".format(name=api['name'],
                                                                                         parameters=parameters,
                                                                                         returns=entity["name"])
        if api['type'] in ['GET', 'GET_ALL']:
            if parameters.strip():
                queries_entities.append(operation_code)
        elif api['type'] in ['POST', 'DELETE', 'PUT']:
            if parameters.strip():
                mutations_entities.append(operation_code)
    return ''.join(queries_entities), ''.join(mutations_entities)


def generate_parameters(entity, api):
    if api['type'] in ['GET', 'DELETE']:
        parameters = ',\n    '.join(
            ['{}: {}!'.format(field['name'], type_mapping.get(field['type'], field['type'])) for field in
             entity['fields'] if field['name'] in entity['primary_key']])
    elif api['type'] == 'POST':
        parameters_ = ['{}: {}!'.format(field['name'], type_mapping.get(field['type'], field['type']))
                       for field in entity['fields'] if field['name'] in entity['primary_key']]
        parameters_ += ['{}: {}!'.format(param, type_mapping.get(
            next((field['type'] for field in entity['fields'] if field['name'] == param), param)))
                        for param in api['parameters']]
        parameters = ',\n   '.join(parameters_)

    else:
        parameters = f"{entity['name']}: {entity['name']}Input!"
    return parameters
