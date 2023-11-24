def generate_event_parse() -> str:
    return """import functools


def parse_event(*params):
    def decorator_parse_event(func):

        @functools.wraps(func)
        def wrapper_parse_event(*args, **kwargs):
            if len(params) < 1 or not callable(params[0]):
                return {'errors': {'message': "Missing params"}}

            if len(args) <= 0 or not isinstance(args[0], dict):
                return {'errors': {'message': "Missing params"}}

            view_model_class = params[0]
            event: dict = args[0]
            try:
                view_model = view_model_class(**event)
            except Exception:
                return {'errors': {'message': "Error parsing event"}}

            args = args + (view_model,)
            return func(*args, **kwargs)

        return wrapper_parse_event

    return decorator_parse_event
    """