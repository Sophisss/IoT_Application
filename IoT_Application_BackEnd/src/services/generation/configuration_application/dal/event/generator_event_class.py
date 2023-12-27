def generate_event_class() -> str:
    """
    This function generates the event class.
    :return: The event class.
    """
    return """from pydantic import BaseModel


class Event(BaseModel):
    field: str
    arguments: dict
    projection: list
    """