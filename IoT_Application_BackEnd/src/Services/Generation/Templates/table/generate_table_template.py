def generate_table_template(json: dict) -> str:
    """
    This function generates the DynamoDB table-related CloudFormation template.
    :param json: the JSON data.
    :return: the DynamoDB table-related CloudFormation template.
    """
    returns = []
    for resource in json:
        new_resource = f"""
  {resource['tableName']}Table:
    Type: AWS::DynamoDB::Table
    Properties: {generate_properties_table(resource)}
          """
        returns.append(new_resource)
    return "".join(returns)


def generate_properties_table(resource: dict) -> str:
    """
    This function generates the DynamoDB table properties.
    :param resource: the resource.
    :return: the DynamoDB table properties.
    """
    GSI = resource.get('GSI', None)

    properties = f"""
      TableName: {resource['tableName']}
      AttributeDefinitions: {generate_attributes_table(resource)}
      KeySchema:{generate_key_schema_table(resource)}
      ProvisionedThroughput:
        ReadCapacityUnits: 5
        WriteCapacityUnits: 5"""

    if GSI:
        properties += f"""
      GlobalSecondaryIndexes: {generate_gsi_table(resource)}
        """

    return properties


def generate_attributes_table(resource: dict) -> str:
    """
    This function generates the DynamoDB table attributes.
    :param resource: the resource.
    :return: the DynamoDB table attributes.
    """
    attribute_mappings = {"String": "S", "Number": "N", "Binary": "B"}
    return f"""
        - AttributeName: {resource['partition_key']['name']}
          AttributeType: {attribute_mappings[resource['partition_key']['type']]}
        - AttributeName: {resource['sort_key']['name']}
          AttributeType: {attribute_mappings[resource['sort_key']['type']]}"""


def generate_key_schema_table(resource: dict) -> str:
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


def generate_gsi_table(resource: dict) -> str:
    """
    This function generates the DynamoDB table GSI.
    :param resource: the resource.
    :return: the DynamoDB table GSI.
    """
    return f"""
        - IndexName: {resource['GSI']['index_name']}
          KeySchema:  {generate_key_schema_gsi(resource)}
          Projection:
            ProjectionType: ALL
          ProvisionedThroughput:
            ReadCapacityUnits: 5
            WriteCapacityUnits: 5"""


def generate_key_schema_gsi(resource: dict) -> str:
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
