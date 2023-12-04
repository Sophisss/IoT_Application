from services.generation.dal.lambda_functions.generate_case_entity import get_links_associated


def generate_entity_relation(entity, links, table_configuration):
    pr_key = table_configuration['partition_key']['name']
    sr_key = table_configuration['sort_key']['name']
    gsi_index = table_configuration['GSI']['index_name']
    separator = table_configuration['parameters']['id_separator']
    link_associated_first_entity, link_associated_second_entity = get_links_associated(entity, links)
    return f"""
{generate_entity_relation_case_first_entity(entity, link_associated_first_entity, pr_key, sr_key, gsi_index, separator)}
{generate_entity_relation_case_second_entity(entity, link_associated_second_entity, pr_key, sr_key, gsi_index, separator)}
"""


def generate_entity_relation_case_first_entity(entity, link_associated_first_entity, pr_key, sr_key, gsi_index,
                                               separator):
    mapping = {"one-to-many": generate_relation_one_to_many_or_many_to_many_first_entity,
               "many-to-one": generate_relation_many_to_one_or_one_to_one_first_entity,
               "many-to-many": generate_relation_one_to_many_or_many_to_many_first_entity,
               "one-to-one": generate_relation_many_to_one_or_one_to_one_first_entity}
    return "".join(
        mapping[link["numerosity"]](entity, link, pr_key, sr_key, gsi_index, separator) for link in
        link_associated_first_entity)


def generate_entity_relation_case_second_entity(entity, link_associated_second_entity, pr_key, sr_key, gsi_index,
                                                separator):
    mapping = {"one-to-many": generate_relation_one_to_many_or_one_to_one_second_entity,
               "many-to-one": generate_relation_many_to_one_or_many_to_many_second_entity,
               "many-to-many": generate_relation_many_to_one_or_many_to_many_second_entity,
               "one-to-one": generate_relation_one_to_many_or_one_to_one_second_entity}
    return "".join(
        mapping[link["numerosity"]](entity, link, pr_key, sr_key, gsi_index, separator) for link in
        link_associated_second_entity)


def generate_relation_one_to_many_or_one_to_one_second_entity(entity, link, pr_key, sr_key, gsi_index, separator):
    return f"""    def get_{link['first_entity'].lower()}_for_{entity['name'].lower()}(self,{link['primary_key'][1]} ) -> dict:
        query = Key('{sr_key}').eq(f'{entity['name']}:{{{link['primary_key'][1]}}}') & Key('{pr_key}').begins_with('{link['first_entity']}')
        response = self.get_items('{entity['table']}', query, index='{gsi_index}')
        return self.get_{link['first_entity'].lower()}(response[0]['{pr_key}'].split('{separator}')[1])
"""


def generate_relation_many_to_one_or_many_to_many_second_entity(entity, link, pr_key, sr_key, gsi_index, separator):
    return f"""    def get_all_{link['first_entity'].lower()}_for_{entity['name'].lower()}(self, {link['primary_key'][1]}) -> list:
        query = Key('{sr_key}').eq(f'{entity['name']}:{{{link['primary_key'][1]}}}') & Key('{pr_key}').begins_with('{link['first_entity']}')
        response = self.get_items('{entity['table']}', query, index='{gsi_index}')
        return list(map(lambda {link['first_entity'].lower()}: self.get_{link['first_entity'].lower()}({link['first_entity'].lower()}['{pr_key}'].split('{separator}')[1]), response))
"""


def generate_relation_one_to_many_or_many_to_many_first_entity(entity, link, pr_key, sr_key, gsi_index, separator):
    return f"""    def get_all_{link['second_entity'].lower()}_for_{entity['name'].lower()}(self, {link['primary_key'][0]}) -> list:
        query = Key('{pr_key}').eq(f'{entity['name']}:{{{link['primary_key'][0]}}}') & Key('{sr_key}').begins_with('{link['second_entity']}')
        response = self.get_items('{entity['table']}', query)
        return list(map(lambda {link['second_entity'].lower()}: self.get_{link['second_entity'].lower()}({link['second_entity'].lower()}['{sr_key}'].split('{separator}')[1]), response))
"""


def generate_relation_many_to_one_or_one_to_one_first_entity(entity, link, pr_key, sr_key, gsi_index, separator):
    return f"""    def get_{link['second_entity'].lower()}_for_{entity['name'].lower()}(self, {link['primary_key'][0]}) -> dict:
        query = Key('{pr_key}').eq(f'{entity['name']}:{{{link['primary_key'][0]}}}') & Key('{sr_key}').begins_with('{link['second_entity']}')
        response = self.get_items('{entity['table']}', query)
        return self.get_{link['second_entity'].lower()}(response[0]['{sr_key}'].split('{separator}')[1])
"""

