def generate_header_lambda(name):

    return f"""from dal.response_manager.exception_class import InvalidApiError
from dal.dynamo_manager.project_dynamo_manager import ProvaDynamoManager
from dal.response_manager import check_response_status, check_response_item
from dal.utility import change_name_keys
from event.event import Event
from event.event_parse import parse_event
from model.{name.lower()} import {name}
"""
