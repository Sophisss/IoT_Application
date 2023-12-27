def generate_lambda_definition(name, name_project):
    return f"""
@parse_event(Event)
def lambda_handler_{name.lower()}(event, context, event_parse: Event, project_manager: {name_project}DynamoManager):
    try:
        match event_parse.field:"""

