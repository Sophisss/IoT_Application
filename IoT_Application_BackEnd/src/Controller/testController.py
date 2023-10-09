import json


def handler(event, context):
    request_data = json.loads(event['body'])
    entity_name = request_data.get('entityname')

    # Imposta le intestazioni CORS
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps({
            "message": f"{entity_name}",
        })
    }
