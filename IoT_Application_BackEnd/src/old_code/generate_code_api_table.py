def add_table_template(json_data_tables, template):
    """
    This function add the DynamoDB table to the CloudFormation template.
    :param json_data_tables: The JSON data of the tables.
    :param template: The CloudFormation template.
    :return: The CloudFormation template with the DynamoDB table.
    """
    for table in json_data_tables:
        template['Resources'][f'{table["tableName"]}Table'] = {
            "Type": "AWS::DynamoDB::Table",
            "Properties": add_properties_table_template(table)
        }


def add_properties_table_template(table):
    """
    This function add the table properties to the CloudFormation template.
    :param table: The table to add the properties.
    :return: The table properties.
    """
    GSI = table.get('GSI', None)

    properties = {
        "TableName": table["tableName"],
        "AttributeDefinitions": add_attributes_template(table),
        "KeySchema": add_key_schema_template(table, is_primary_key=True),
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    }

    if GSI:
        properties["GlobalSecondaryIndexes"] = add_gsi_template(table)

    return properties


def add_attributes_template(table):
    """
    This function add the table attributes to the CloudFormation template.
    :param table: The table to add the attributes.
    :return: The table attributes.
    """
    attribute_mappings = {"String": "S", "Number": "N", "Binary": "B"}
    return [
        {"AttributeName": table['partition_key']["name"],
         "AttributeType": attribute_mappings[table['partition_key']["type"]]},
        {"AttributeName": table['sort_key']["name"], "AttributeType": attribute_mappings[table['sort_key']["type"]]}
    ]


def add_key_schema_template(table, is_primary_key):
    """
    This function add the table key schema to the CloudFormation template.
    :param table: The table to add the key schema.
    :param is_primary_key: Flag indicating whether it's a primary key or not.
    :return: The table key schema.
    """
    key_name = table['partition_key']["name"] if is_primary_key else table['GSI']['partition_key']
    sort_key_name = table['sort_key']["name"] if is_primary_key else table['GSI']['sort_key']
    return [
        {"AttributeName": key_name, "KeyType": "HASH"},
        {"AttributeName": sort_key_name, "KeyType": "RANGE"}
    ]


def add_gsi_template(table):
    """
    This function add the table global secondary indexes to the CloudFormation template.
    :param table: The table to add the global secondary indexes.
    :return: The table global secondary indexes.
    """
    return [
        {
            "IndexName": table['GSI']['index_name'],
            "KeySchema": add_key_schema_template(table, is_primary_key=False),
            "Projection": {
                "ProjectionType": "ALL"
            },
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        }
    ]
