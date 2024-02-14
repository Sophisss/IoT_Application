def generate_device_status_event() -> str:
    """
    This function generates the DeviceStatusEvent class.
    :return: The DeviceStatusEvent class.
    """
    return """from iot.models.device_status_change import DeviceStatusChange


class DeviceStatusEvent:
    device_id: str
    changes: [DeviceStatusChange]

    def __init__(self, device_id: str, changes: [DeviceStatusChange]):
        self.device_id = device_id
        self.changes = changes
        """