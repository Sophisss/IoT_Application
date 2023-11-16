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
      KeySchema:{generate_key_schema_table(resource, is_primary_key=True)}
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
        - AttributeName: {resource['partition_key']['name']}
          AttributeType: {attribute_mappings[resource['partition_key']['type']]}
        - AttributeName: {resource['sort_key']['name']}
          AttributeType: {attribute_mappings[resource['sort_key']['type']]}"""


def generate_key_schema_table(resource: dict, is_primary_key: bool) -> str:
    """
    This function generates the DynamoDB table key schema.
    :param resource: the resource.
    :param is_primary_key: Flag indicating whether it's a primary key or not.
    :return: the DynamoDB table key schema.
    """
    key_name = resource['partition_key']['name'] if is_primary_key else resource['GSI']['partition_key']
    sort_key_name = resource['sort_key']['name'] if is_primary_key else resource['GSI']['sort_key']
    return f"""
        - AttributeName: {key_name}
          KeyType: HASH
        - AttributeName: {sort_key_name}
          KeyType: RANGE"""


def generate_gsi_table(resource: dict) -> str:
    """
    This function generates the DynamoDB table GSI.
    :param resource: the resource.
    :return: the DynamoDB table GSI.
    """
    return f"""
        - IndexName: {resource['GSI']['index_name']}
          KeySchema:  {generate_key_schema_table(resource, is_primary_key=False)}
          Projection:
            ProjectionType: ALL
          ProvisionedThroughput:
            ReadCapacityUnits: 5
            WriteCapacityUnits: 5"""
