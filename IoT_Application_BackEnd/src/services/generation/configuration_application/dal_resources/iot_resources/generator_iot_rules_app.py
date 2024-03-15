import re


def generate_iot_rules_app(json: dict) -> str:
    return f"""{__generate_header()}
{__generate_lambdas(json)}
{__generate_get_event()}
{__generate_device_status_storage()}
    """


def __generate_header() -> str:
    return """from timestream_manager.timeseries_dal import TimeseriesDal
from timestream_manager.project_timeseries_manager import IoT_PlatformTimeseriesManager
from iot.device_status_event import DeviceStatusEvent
from iot.device_status_change import DeviceStatusChange
    """


def __generate_lambdas(json: dict) -> str:
    iot_rule = json['awsConfig']['iot']['iot_rule']
    rule_section = iot_rule['rule']
    sql_statement = rule_section['sql_statement'] if rule_section else None

    if sql_statement:
        resources = __generate_monitor_device_status_mqtt(sql_statement)
        if iot_rule['shadow_notify']:
            resources += __generate_monitor_device_status_shadow()
        return resources
    else:
        return __generate_monitor_device_status_shadow()


def __generate_monitor_device_status_shadow() -> str:
    return """
    
def monitor_device_status_shadow(event, _):
    device_id = event['thingName']
    device_status_reported = event['current']['state']['reported']

    event = get_event(device_id, device_status_reported)
    device_status_storage(event)
    """


def __generate_monitor_device_status_mqtt(sql_statement: str) -> str:
    is_present = '*' in sql_statement
    select_fields = extract_select_fields(sql_statement)
    filtered_fields = list(field for field in select_fields if field.split(' AS ', 1)[1] != 'thingName') if not is_present else select_fields

    code = if_is_present() if is_present else not_is_present(filtered_fields)

    return f"""
def monitor_device_status_mqtt(event, _):
{code}
    device_status_storage(event)
"""


def extract_select_fields(sql_statement: str):
    fields = re.findall(r'SELECT\s+(.*?)\s+FROM', sql_statement, re.IGNORECASE)
    return list(map(lambda f: f.strip(), fields[0].split(','))) if fields else []


def if_is_present() -> str:
    return """    thingName = event['thingName']
    del event['thingName']
    
    event = get_event(thingName, event)"""


def not_is_present(filtered_fields) -> str:
    return f"""    thingName = event['thingName']
{__generate_variables(filtered_fields)}
{__generate_device_status_dict(filtered_fields)}

    event = get_event(thingName, device_status)"""


def __generate_variables(filtered_fields: list) -> str:
    return '\n'.join(
        map(lambda field: f"    {field.split(' AS ', 1)[0]} = event['{field.split(' AS ', 1)[1]}']", filtered_fields))


def __generate_device_status_dict(filtered_fields: list) -> str:
    return f"""    device_status = {{
{''.join(map(lambda field: f"        '{field.split(' AS ')[1].strip()}': {field.split(' AS ')[0].strip()},", filtered_fields))}
    }}"""


def __generate_get_event() -> str:
    return """
def get_event(device_id: str, status: dict) -> DeviceStatusEvent:
    device_status_changes = []
    for signal, value in status.items():
        device_status_changes.append(DeviceStatusChange(value, signal))

    return DeviceStatusEvent(device_id, device_status_changes)
    """


def __generate_device_status_storage() -> str:
    return """
def device_status_storage(event: DeviceStatusEvent):
    try:
        device_id = event.device_id
        changes = event.changes

        timeseries_manager = IoT_PlatformTimeseriesManager()
        timeseries_manager.write_device_changes(device_id, changes)
    except Exception as e:
        return {'errors': {'message': 'An error occurred during device status monitoring.',
                           'type': str(e.__class__.__name__)}}
    """
