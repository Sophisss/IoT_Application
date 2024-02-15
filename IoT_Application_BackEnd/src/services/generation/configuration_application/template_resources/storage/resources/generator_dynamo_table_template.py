from services.generation.utility_methods import get_dynamo_data


def generate_dynamo_table_template(json: dict) -> str:
    """
    This function generates the DynamoDB table resources.
    :param json: the JSON object.
    :return: the DynamoDB table resources.
    """
    dynamo_tables = get_dynamo_data(json)
    return "".join(map(lambda resource: __generate_table_resource(resource), dynamo_tables))


def __generate_table_resource(table: dict) -> str:
    """
    This function generates the resource definition for a DynamoDB table.
    :param table: the table.
    :return: the resource definition for a DynamoDB table.
    """
    return f"""
  {table['tableName']}Table:
    Type: AWS::DynamoDB::Table
    Properties: {__generate_table_properties(table)}      
    """


def __generate_table_properties(table: dict) -> str:
    """
    This function generates the DynamoDB table properties.
    :param table: the table.
    :return: the DynamoDB table properties.
    """
    return f"""
      TableName: {table['tableName']}
      AttributeDefinitions: {__generate_table_attributes(table)}
      KeySchema:{__generate_key_schema_table(table)}
      ProvisionedThroughput:
        ReadCapacityUnits: 5
        WriteCapacityUnits: 5
{__generate_gsi(table)}"""


def __generate_table_attributes(table: dict) -> str:
    """
    This function generates the DynamoDB table attributes.
    :param table: the table.
    :return: the DynamoDB table attributes.
    """
    attribute_mappings = {"string": "S", "number": "N", "binary": "B"}
    return f"""
        - AttributeName: {table['partition_key']['name']}
          AttributeType: {attribute_mappings[table['partition_key']['type']]}
        - AttributeName: {table['sort_key']['name']}
          AttributeType: {attribute_mappings[table['sort_key']['type']]}"""


def __generate_key_schema_table(table: dict) -> str:
    """
    This function generates the DynamoDB table key schema.
    :param table: the resource.
    :return: the DynamoDB table key schema.
    """
    return f"""
        - AttributeName: {table['partition_key']['name']}
          KeyType: HASH
        - AttributeName: {table['sort_key']['name']}
          KeyType: RANGE"""


def __generate_gsi(table: dict) -> str:
    """
    This function generates the DynamoDB table GSI.
    :param table: the table.
    :return: the DynamoDB table GSI if it exists or an empty string otherwise.
    """
    return f"""      GlobalSecondaryIndexes: {__generate_gsi_resources(table)}
      """ if table.get('GSI', None) else ""


def __generate_gsi_resources(table: dict) -> str:
    """
    This function generates the DynamoDB table GSI.
    :param table: the resource.
    :return: the DynamoDB table GSI.
    """
    return f"""
        - IndexName: {table['GSI']['index_name']}
          KeySchema:  {__generate_key_schema_gsi(table)}
          Projection:
            ProjectionType: ALL
          ProvisionedThroughput:
            ReadCapacityUnits: 5
            WriteCapacityUnits: 5"""


def __generate_key_schema_gsi(table: dict) -> str:
    """
    This function generates the DynamoDB table GSI key schema.
    :param table: the table.
    :return: the DynamoDB table GSI key schema.
    """
    return f"""
            - AttributeName: {table['GSI']['partition_key']}
              KeyType: HASH
            - AttributeName: {table['GSI']['sort_key']}
              KeyType: RANGE"""
