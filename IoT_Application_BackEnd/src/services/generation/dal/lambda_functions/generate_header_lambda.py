def generate_header_lambda(name, name_project):

    return f"""from dal.response_manager.exception_class import *
from dal.dynamo_manager.project_dynamo_manager import {name_project}DynamoManager
from dal.response_manager.response_manager import check_response_status, check_response_item
from dal.utility import change_name_keys
from event.event import Event
from event.event_parse import parse_event
from model.{name.lower()} import {name}
"""
