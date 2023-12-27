def generate_table_template(json: dict) -> str:
    """
    This function generates the CloudFormation template for DynamoDB table.
    :param json: JSON data containing DynamoDB table configuration.
    :return: the DynamoDB table-related CloudFormation template.
    """
    return "".join(map(lambda resource: __generate_table_resource(resource), json))


def __generate_table_resource(resource: dict) -> str:
    """
    This function generates the resource definition for a DynamoDB table.
    :param resource: the resource data.
    :return: the resource definition for a DynamoDB table.
    """
    return f"""
  {resource['tableName']}Table:
    Type: AWS::DynamoDB::Table
    Properties: {__generate_table_properties(resource)}      
    """


def __generate_table_properties(resource: dict) -> str:
    """
    This function generates the DynamoDB table properties.
    :param resource: the resource.
    :return: the DynamoDB table properties.
    """
    return f"""
      TableName: {resource['tableName']}
      AttributeDefinitions: {__generate_table_attributes(resource)}
      KeySchema:{__generate_key_schema_table(resource)}
      ProvisionedThroughput:
        ReadCapacityUnits: 5
        WriteCapacityUnits: 5
{__generate_gsi(resource)}"""


def __generate_table_attributes(resource: dict) -> str:
    """
    This function generates the DynamoDB table attributes.
    :param resource: the resource.
    :return: the DynamoDB table attributes.
    """
    attribute_mappings = {"string": "S", "number": "N", "binary": "B"}
    return f"""
        - AttributeName: {resource['partition_key']['name']}
          AttributeType: {attribute_mappings[resource['partition_key']['type']]}
        - AttributeName: {resource['sort_key']['name']}
          AttributeType: {attribute_mappings[resource['sort_key']['type']]}"""


def __generate_key_schema_table(resource: dict) -> str:
    """
    This function generates the DynamoDB table key schema.
    :param resource: the resource.
    :return: the DynamoDB table key schema.
    """
    return f"""
        - AttributeName: {resource['partition_key']['name']}
          KeyType: HASH
        - AttributeName: {resource['sort_key']['name']}
          KeyType: RANGE"""


def __generate_gsi(resource: dict) -> str:
    """
    This function generates the DynamoDB table GSI.
    :param resource: the resource.
    :return: the DynamoDB table GSI if it exists or an empty string otherwise.
    """
    return f"""      GlobalSecondaryIndexes: {__generate_gsi_resources(resource)}
      """ if resource.get('GSI', None) else ""


def __generate_gsi_resources(resource: dict) -> str:
    """
    This function generates the DynamoDB table GSI.
    :param resource: the resource.
    :return: the DynamoDB table GSI.
    """
    return f"""
        - IndexName: {resource['GSI']['index_name']}
          KeySchema:  {__generate_key_schema_gsi(resource)}
          Projection:
            ProjectionType: ALL
          ProvisionedThroughput:
            ReadCapacityUnits: 5
            WriteCapacityUnits: 5"""


def __generate_key_schema_gsi(resource: dict) -> str:
    """
    This function generates the DynamoDB table GSI key schema.
    :param resource: the resource.
    :return: the DynamoDB table GSI key schema.
    """
    return f"""
            - AttributeName: {resource['GSI']['partition_key']}
              KeyType: HASH
            - AttributeName: {resource['GSI']['sort_key']}
              KeyType: RANGE"""
