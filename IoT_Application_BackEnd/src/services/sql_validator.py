import json
import sqlvalidator


def validate_sql_instructions(event, _):
    print(event)
    body = json.loads(event['body'])
    topic = body['topic']
    select_fields = body['select_fields']

    sql_query = f"SELECT {', '.join(select_fields)} FROM {topic}"

    result = sqlvalidator.parse(sql_query)

    if not result.is_valid:
        return {
            "message": "SQL query is invalid"
        }

    return {
        "message": "SQL query is valid"
    }
