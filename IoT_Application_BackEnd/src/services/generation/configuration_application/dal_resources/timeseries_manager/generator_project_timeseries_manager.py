from services.generation.utility_methods import get_timestream_data


def generate_project_timeseries_manager(json_data: dict) -> str:
    """
    This function generates the timeseries manager class for the project.
    :param json_data: The json data from the project configuration file.
    :return: The timeseries manager class for the project.
    """
    return f"""{__generate_header()}
{__generate_class(json_data)}
    """


def __generate_header() -> str:
    """
    This function generates the header of the timeseries manager class.
    :return: The header of the timeseries manager class.
    """
    return """from timestream_manager.timeseries_dal import TimeseriesDal
from iot.device_status_change import DeviceStatusChange
    """


def __generate_class(json_data: dict) -> str:
    """
    This function generates the timeseries manager class.
    :param json_data: The json data from the project configuration file.
    :return: The timeseries manager class.
    """
    return f"""class IoT_PlatformTimeseriesManager(TimeseriesDal):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IoT_PlatformTimeseriesManager, cls).__new__(cls)
        return cls._instance
        
{__generate_methods(json_data)}"""


def __generate_methods(json_data: dict) -> str:
    """
    This function generates the methods of the timeseries manager class.
    :param json_data: The json data from the project configuration file.
    :return: The methods of the timeseries manager class.
    """
    return f"""{__generate_write_device_changes(json_data)}
    """


def __generate_write_device_changes(json_data: dict) -> str:
    """
    This function generates the write device changes method.
    :param json_data: The json data from the project configuration file.
    :return: The write device changes method.
    """
    database_name, table_name = get_timestream_data(json_data)

    return f"""    def write_device_changes(self, device_id: str, changes: [DeviceStatusChange]):
        if not device_id or not changes or len(changes) <= 0:
            raise ValueError("Invalid parameters")

        self.write_device_status_changes(device_id, '{database_name}', '{table_name}', changes)
    """
