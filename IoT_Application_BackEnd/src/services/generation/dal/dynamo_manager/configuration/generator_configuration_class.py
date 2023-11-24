def generate_configuration_class() -> str:
    """
    This function generates the configuration class.
    :return: The configuration class.
    """
    return """class Configuration:
    def __init__(self, table_name, separator, partition_key_table, sort_key_table, single_entity_storage_keyword, gsi):
        self.table = table_name
        self.separator = separator
        self.partition_key_table = partition_key_table
        self.sort_key_table = sort_key_table
        self.single_entity_storage_keyword = single_entity_storage_keyword
        self.gsi = gsi
    """