file_result_template = """
{configuration_dynamo}
{lambdas}
{lambdas_link}
"""

template_configuration_dynamo = """
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('{table_name}')
separator = '{separator}'
single_entity_storage_keyword = '{single_entity_storage_keyword}'
partition_key_table = '{partition_key}'
sort_key_table = '{sort_key}'
"""

template_lambda_handler = """
def lambda_handler_{name_entity}(event, context):
    {match}
    {methods}
        case _:
            response = 'error'
    return response
"""

template_method_for_get = """
        case '{name_method}':
             {primary_key} = event['arguments']['{primary_key}']
             {primary_key} = f"{name_entity}{{separator}}{{{primary_key}}}"
             {option}
             response = table.get_item(Key={{
                 partition_key_table: {primary_key},
                 sort_key_table: single_entity_storage_keyword
                 }})
             response = response['Item']
             response['{primary_key}'] = response.pop(partition_key_table)"""
option_template_for_link = """
             if '{second_entity}' in event['projection']:
                response = table.query(
                    KeyConditionExpression=(
                        Key(partition_key_table).eq({primary_key})
                    )
                )
                result = []
                for item in response['Items']:
                    if item[sort_key_table] == single_entity_storage_keyword :
                        item['{primary_key}'] = item.pop(partition_key_table)
                        response = item
                    else:
                        response_query = table.get_item(Key={{
                            partition_key_table: item[sort_key_table],
                            sort_key_table: single_entity_storage_keyword
                        }})
                        response_query = response_query['Item']
                        response_query['{primary_key}'] = response_query.pop(partition_key_table)
                        result.append(response_query)
                response['{second_entity}'] = result"""

template_method_for_delete = """
        case '{name_method}':
            {primary_key} = event['arguments']['{primary_key}']
            {primary_key} = f"{name_entity}{{separator}}{{{primary_key}}}"
            response = table.delete_item(Key={{
                partition_key_table: {primary_key},
                sort_key_table: single_entity_storage_keyword
              }}, ReturnValues='ALL_OLD')
            response = response['Attributes']
            response['{primary_key}'] = response.pop(partition_key_table)"""

template_method_for_create = """
        case '{name_method}':
            {primary_key} = event['arguments']['{name_entity}']['{primary_key}']
            {primary_key} = f"{name_entity}{{separator}}{{{primary_key}}}"
            arguments = event['arguments']['{name_entity}']
            del arguments['{primary_key}']
            arguments[partition_key_table]={primary_key}
            arguments[sort_key_table] = single_entity_storage_keyword
            table.put_item(Item=arguments)
            response = arguments"""

template_lambda_handler_link = """
def lambda_handler_{first_entity}{second_entity}_link(event, context):
    {partition_key} = event['arguments']['{partition_key}']
    {partition_key} = f"{first_entity}{{separator}}{{{partition_key}}}"
    {sort_key} = event['arguments']['{sort_key}']
    {sort_key} = f"{second_entity}{{separator}}{{{sort_key}}}"
    {match}
         {methods}
        case _: 
            response = 'error'
    return response"""

template_method_for_create_link = """
        case '{name_method}':
            arguments = event['arguments']
            arguments[partition_key_table] = arguments.pop({partition_key})
            arguments[sort_key_table] = arguments.pop({sort_key})
            response = table.put_item(Item=arguments)
            response = arguments"""
template_method_for_get_link = """
        case '{name_method}':
            response = table.put_item(Key={{
                partition_key_table: {partition_key},
                sort_key_table: {sort_key}
            }})
            response = response['Item']
            response['{partition_key}'] = response.pop(partition_key_table)
            response['{sort_key}'] = response.pop(sort_key_table)"""
template_method_for_delete_link = """
        case '{name_method}':
            response = table.delete_item(Key={{
                partition_key_table: {partition_key},
                sort_key_table: {sort_key}
              }}, ReturnValues='ALL_OLD')
            response = response['Attributes']
            response['{partition_key}'] = response.pop(partition_key_table)
            response['{sort_key}'] = response.pop(sort_key_table)"""
