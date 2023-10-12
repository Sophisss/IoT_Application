import json


def handler(event, context):
    request_data = json.loads(event['body'])
    # Imposta le intestazioni CORS
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    return {
        "statusCode": 200,
        "headers": headers
    }
