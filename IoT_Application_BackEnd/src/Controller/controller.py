import json
import boto3


dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
table = dynamodb.Table("IoT")


def getDevice(event, context):
    primary_key = event["arguments"]["primary_key"]

    response = table.get_item(Key={
        'partitionKey': primary_key,
        'datatype': 'registry'
    })

    item = response.get('Item')

    if item and response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {
            'statusCode': 200,
            'body': json.dumps(item)
        }
    elif not item:
        return {
            'statusCode': 404,
            'body': json.dumps({
                'message': 'Item not found'
            })
        }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error while getting item'
            })
        }

