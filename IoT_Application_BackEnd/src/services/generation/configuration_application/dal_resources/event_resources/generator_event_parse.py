def generate_event_parse(json: dict) -> str:
    """
    This function generates the event parse for the DAL template.
    :return: The event parse for the DAL template.
    """
    return f"""import functools
from dal.dynamo_manager.project_dynamo_manager import {json['projectName']}DynamoManager


def parse_event(*params):
    def decorator_parse_event(func):

        @functools.wraps(func)
        def wrapper_parse_event(*args, **kwargs):
            if len(params) < 1 or not callable(params[0]):
                return {{'errors': {{'message': "Missing params"}}}}

            if len(args) <= 0 or not isinstance(args[0], dict):
                return {{'errors': {{'message': "Missing params"}}}}

            view_model_class = params[0]
            event: dict = args[0]
            try:
                view_model = view_model_class(**event)
                project_dynamo_manager_instance = {json['projectName']}DynamoManager()
            except Exception:
                return {{'errors': {{'message': "Error parsing event"}}}}

            args = args + (view_model,) + (project_dynamo_manager_instance,)
            return func(*args, **kwargs)

        return wrapper_parse_event

    return decorator_parse_event
    """
