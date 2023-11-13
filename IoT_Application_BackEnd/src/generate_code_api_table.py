# Function that add the DynamoDB table to the CloudFormation template.
def add_table_template(json_data_tables, template):
    for table in json_data_tables:
        new_resources = {
            f'{table["tableName"]}Table': {
                "Type": "AWS::DynamoDB::Table",
                "Properties": add_properties_table_template(table)
            }
        }
        template['Resources'].update(new_resources)


# Function that add the table properties to the CloudFormation template.
def add_properties_table_template(table):
    GSI = table.get('GSI', None)

    properties = {
        "TableName": f"{table['tableName']}",
        "AttributeDefinitions": add_attributes_template(table),
        "KeySchema": add_key_schema_template(table),
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    }

    if GSI:
        properties["GlobalSecondaryIndexes"] = add_gsi_template(table)

    return properties


# Function that add the table attributes to the CloudFormation template.
def add_attributes_template(table):
    attribute_mappings = {"String": "S", "Number": "N", "Binary": "B"}
    return [
        {"AttributeName": table['partition_key']["name"],
         "AttributeType": attribute_mappings[table['partition_key']["type"]]},
        {"AttributeName": table['sort_key']["name"], "AttributeType": attribute_mappings[table['sort_key']["type"]]}
    ]


# Function that add the table key schema to the CloudFormation template.
def add_key_schema_template(table):
    return [
        {"AttributeName": table['partition_key']["name"], "KeyType": "HASH"},
        {"AttributeName": table['sort_key']["name"], "KeyType": "RANGE"}
    ]


# Function that add the table global secondary indexes to the CloudFormation template.
def add_gsi_template(table):
    return [
        {
            "IndexName": table['GSI']['index_name'],
            "KeySchema": [
                {"AttributeName": table['GSI']['partition_key'], "KeyType": "HASH"},
                {"AttributeName": table['GSI']['sort_key'], "KeyType": "RANGE"}
            ],
            "Projection": {
                "ProjectionType": "ALL"
            },
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        }
    ]
