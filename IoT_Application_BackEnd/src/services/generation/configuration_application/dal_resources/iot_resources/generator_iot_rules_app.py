def generate_iot_rules_app() -> str:
    return f"""{__generate_header()}
{__generate_lambdas()}
    """


def __generate_header() -> str:
    """
    This function generates the header of the TimeseriesDal class.
    :return: The header of the TimeseriesDal class.
    """
    return """from timestream_manager.timeseries_dal import TimeseriesDal
from timestream_manager.project_timeseries_manager import IoT_PlatformTimeseriesManager
from iot.device_status_event import DeviceStatusEvent
from iot.device_status_change import DeviceStatusChange
    """


def __generate_lambdas() -> str:
    return f"""{__generate_monitor_device_status_shadow()}
{__generate_monitor_device_status_mqtt()}
{__generate_get_event()}
{__generate_device_status_storage()}
    """


def __generate_monitor_device_status_shadow() -> str:
    return """def monitor_device_status_shadow(event, _):
    device_id = event['thingName']
    device_status_reported = event['current']['state']['reported']

    event = get_event(device_id, device_status_reported)
    device_status_storage(event)
    """


def __generate_monitor_device_status_mqtt() -> str:
    return """def monitor_device_status_mqtt(event, _):
    device_id = event['thingName']
    device_status = event['shadow']['state']['reported']

    event = get_event(device_id, device_status)
    device_status_storage(event)
    """


def __generate_get_event() -> str:
    return """def get_event(device_id: str, status: dict) -> DeviceStatusEvent:
    device_status_changes = []
    for signal, value in status.items():
        device_status_changes.append(DeviceStatusChange(value, signal))

    return DeviceStatusEvent(device_id, device_status_changes)
    """


def __generate_device_status_storage() -> str:
    return """def device_status_storage(event: DeviceStatusEvent):
    try:
        device_id = event.device_id
        changes = event.changes

        timeseries_manager = IoT_PlatformTimeseriesManager()
        timeseries_manager.write_device_changes(device_id, changes)
    except Exception as e:
        return {'errors': {'message': 'An error occurred during device status monitoring.',
                           'type': str(e.__class__.__name__)}}
    """