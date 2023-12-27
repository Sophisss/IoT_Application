def generate_header_lambda(name: str, project_name: str) -> str:
    """
    This function generates the header of the lambda.
    :param name: name of the entity or link.
    :param project_name: name of the project.
    :return: the header of the lambda.
    """
    return f"""from dal.response_manager.exception_class import *
from dal.dynamo_manager.project_dynamo_manager import {project_name}DynamoManager
from dal.response_manager.response_manager import check_response_status, check_response_item
from dal.utility import change_name_keys
from event.event import Event
from event.event_parse import parse_event
from model.{name.lower()} import {name}
"""
