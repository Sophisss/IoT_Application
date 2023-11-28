from services.generation.dal.dynamo_manager.configuration.generator_methods import generate_configuration_methods


def generate_configuration_class() -> str:
    """
    This function generates the configuration class.
    :return: The configuration class generated.
    """
    return f"""import boto3


class Configuration:
{__generate_constructor()}
{__generate_methods()}
    """


def __generate_constructor() -> str:
    """
    This function generates the constructor of the configuration class.
    :return: The constructor of the configuration class.
    """
    return """    def __init__(self, table_name, separator, partition_key_table, sort_key_table, single_entity_storage_keyword, gsi):
        self.table = self.__instance_table(table_name)
        self.separator = separator
        self.partition_key_table = partition_key_table
        self.sort_key_table = sort_key_table
        self.single_entity_storage_keyword = single_entity_storage_keyword
        self.gsi = gsi"""


def __generate_methods() -> str:
    """
    This function generates the methods of the configuration class.
    :return: The methods of the configuration class.
    """
    return f"""{generate_configuration_methods()}
    """
