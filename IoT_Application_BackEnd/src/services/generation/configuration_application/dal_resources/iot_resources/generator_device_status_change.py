def generate_device_status_change() -> str:
    """
    This function generates the DeviceStatusChange class.
    :return: The DeviceStatusChange class.
    """
    return """class DeviceStatusChange:
    new_value: None
    signal: None

    def __init__(self, new_value, signal):
        self.new_value = new_value
        self.signal = signal
        """


