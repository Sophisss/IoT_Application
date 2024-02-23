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
    topic = iot_rule['topic'] if iot_rule else None

    if topic:
        resources = __generate_monitor_device_status_mqtt()
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


# TODO: rivedi device_status

def __generate_monitor_device_status_mqtt() -> str:
    return """
def monitor_device_status_mqtt(event, _):
    device_id = event['thingName']
    device_status = event['shadow']['state']['reported']

    event = get_event(device_id, device_status)
    device_status_storage(event)
    """


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