def generate_lambda_definition(name: str, project_name: str) -> str:
    """
    This function generates the lambda definition.
    :param name: the name of the entity or link.
    :param project_name: the name of the project.
    :return: the lambda definition.
    """
    return f"""
@parse_event(Event)
def lambda_handler_{name.lower()}(event, context, event_parse: Event, project_manager: {project_name}DynamoManager):
    try:
        match event_parse.field:"""
