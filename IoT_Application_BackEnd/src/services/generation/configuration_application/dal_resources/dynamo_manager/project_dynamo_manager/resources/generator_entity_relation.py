from services.generation.utility_methods import get_links_associated


def generate_entity_relation(entity: dict, links: list, table_configuration: dict) -> str:
    pr_key = table_configuration['partition_key']['name']
    sr_key = table_configuration['sort_key']['name']
    gsi_index = table_configuration['GSI']['index_name']
    separator = table_configuration['parameters']['id_separator']
    links_associated_first_entity, links_associated_second_entity = get_links_associated(entity, links)
    return f"""
{__generate_entity_relation_case_first_entity(entity, links_associated_first_entity, pr_key, sr_key, gsi_index, separator)}
{__generate_entity_relation_case_second_entity(entity, links_associated_second_entity, pr_key, sr_key, gsi_index, separator)}
"""


def __generate_entity_relation_case_first_entity(entity: dict, links_associated_first_entity: list, pr_key: str, sr_key: str, gsi_index: str,
                                                 separator: str) -> str:
    toReturn = ""
    for link in links_associated_first_entity:
        match link["numerosity"]:
            case "one-to-many":
                toReturn += __generate_relation_one_to_many_or_many_to_many_first_entity(entity, link, pr_key, sr_key, gsi_index, separator)
            case "many-to-one":
                toReturn += __generate_relation_many_to_one_or_one_to_one_first_entity(entity, link, pr_key, sr_key, gsi_index, separator)
            case "many-to-many":
                toReturn += __generate_relation_one_to_many_or_many_to_many_first_entity(entity, link, pr_key, sr_key, gsi_index, separator)
            case "one-to-one":
                toReturn += __generate_relation_many_to_one_or_one_to_one_first_entity(entity, link, pr_key, sr_key, gsi_index, separator)

    return toReturn


def __generate_entity_relation_case_second_entity(entity: dict, links_associated_second_entity: list, pr_key: str, sr_key: str, gsi_index: str,
                                                  separator: str) -> str:
    toReturn = ""
    for link in links_associated_second_entity:
        match link["numerosity"]:
            case "one-to-many":
                toReturn += __generate_relation_one_to_many_or_one_to_one_second_entity(entity, link, pr_key, sr_key, gsi_index, separator)
            case "many-to-one":
                toReturn += __generate_relation_many_to_one_or_many_to_many_second_entity(entity, link, pr_key, sr_key, gsi_index, separator)
            case "many-to-many":
                toReturn += __generate_relation_many_to_one_or_many_to_many_second_entity(entity, link, pr_key, sr_key, gsi_index, separator)
            case "one-to-one":
                toReturn += __generate_relation_one_to_many_or_one_to_one_second_entity(entity, link, pr_key, sr_key, gsi_index, separator)

    return toReturn


def __generate_relation_one_to_many_or_one_to_one_second_entity(entity: dict, link: dict, pr_key: str, sr_key: str, gsi_index: str, separator: str) -> str:
    return f"""    def get_{link['first_entity'].lower()}_for_{entity['name'].lower()}(self, {link['primary_key'][1]}):
        query = Key('{sr_key}').eq(f'{entity['name']}:{{{link['primary_key'][1]}}}') & Key('{pr_key}').begins_with('{link['first_entity']}')
        response = self.get_items('{entity['table']}', query, index='{gsi_index}')
        if not response:
            return response
        else:
            return self.get_{link['first_entity'].lower()}(response[0]['{pr_key}'].split('{separator}')[1])
"""


def __generate_relation_many_to_one_or_many_to_many_second_entity(entity: dict, link: dict, pr_key: str, sr_key: str, gsi_index: str, separator: str) -> str:
    return f"""    def get_all_{link['first_entity'].lower()}_for_{entity['name'].lower()}(self, {link['primary_key'][1]}) -> list:
        query = Key('{sr_key}').eq(f'{entity['name']}:{{{link['primary_key'][1]}}}') & Key('{pr_key}').begins_with('{link['first_entity']}')
        response = self.get_items('{entity['table']}', query, index='{gsi_index}')
        return list(map(lambda {link['first_entity'].lower()}: self.get_{link['first_entity'].lower()}({link['first_entity'].lower()}['{pr_key}'].split('{separator}')[1]), response))
"""


def __generate_relation_one_to_many_or_many_to_many_first_entity(entity: dict, link: dict, pr_key: str, sr_key: str, gsi_index: str, separator: str) -> str:
    return f"""    def get_all_{link['second_entity'].lower()}_for_{entity['name'].lower()}(self, {link['primary_key'][0]}) -> list:
        query = Key('{pr_key}').eq(f'{entity['name']}:{{{link['primary_key'][0]}}}') & Key('{sr_key}').begins_with('{link['second_entity']}')
        response = self.get_items('{entity['table']}', query)
        return list(map(lambda {link['second_entity'].lower()}: self.get_{link['second_entity'].lower()}({link['second_entity'].lower()}['{sr_key}'].split('{separator}')[1]), response))
"""


def __generate_relation_many_to_one_or_one_to_one_first_entity(entity: dict, link: dict, pr_key: str, sr_key: str, gsi_index: str, separator: str) -> str:
    return f"""    def get_{link['second_entity'].lower()}_for_{entity['name'].lower()}(self, {link['primary_key'][0]}):
        query = Key('{pr_key}').eq(f'{entity['name']}:{{{link['primary_key'][0]}}}') & Key('{sr_key}').begins_with('{link['second_entity']}')
        response = self.get_items('{entity['table']}', query)
        if not response:
            return response
        else:
            return self.get_{link['second_entity'].lower()}(response[0]['{sr_key}'].split('{separator}')[1])
"""
