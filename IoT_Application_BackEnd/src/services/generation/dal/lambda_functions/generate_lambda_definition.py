def generate_lambda_definition(name):
    return f"""
@parse_event(Event)
def lambda_handler_{name.lower()}(event, context, event_parse: Event, project_manager: ProvaDynamoManager):
    try:
        match event_parse.field:"""

