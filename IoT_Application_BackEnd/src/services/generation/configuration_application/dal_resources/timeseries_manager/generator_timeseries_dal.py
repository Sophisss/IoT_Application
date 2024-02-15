def generate_timeseries_dal() -> str:
    """
    This function generates TimeseriesDal class.
    :return: The TimeseriesDal class generated.
    """
    return f"""{__generate_header()}
{__generate_class()}
    """


def __generate_header() -> str:
    """
    This function generates the header of the TimeseriesDal class.
    :return: The header of the TimeseriesDal class.
    """
    return """import boto3
import time
from iot.device_status_change import DeviceStatusChange
    """


def __generate_class() -> str:
    """
    This function generates the code for the TimeseriesDal class.
    :return: The code for the TimeseriesDal class.
    """
    return f"""
    
class TimeseriesDal:
    timestream = None
    timestream_write = None

    def __init__(self):
        self.timestream = boto3.client('timestream-query')
        self.timestream_write = boto3.client('timestream-write')
        
{__generate_methods()}"""


def __generate_methods() -> str:
    """
    This function generates the methods for the TimeseriesDal class.
    :return: The methods for the TimeseriesDal class.
    """
    return f"""    # region write operations
{__generate_write_device_status_changes()}
{__generate_write_records()}
    # endregion
    
    # region device status changes writes
{__generate_build_records()}
{__generate_build_common_attributes()}
{__generate_get_value_timestream_type()}
    # endregion
    """


def __generate_write_device_status_changes() -> str:
    """
    This function generates the write_device_status_changes method.
    :return: The write_device_status_changes method.
    """
    return """
    def write_device_status_changes(self, device_id: str, database_name: str, table_name: str, changes: [DeviceStatusChange]):
        if not database_name or not table_name:
            raise ValueError("Database and table names are required.")

        records = self.__build_records(changes)
        common_attributes = self.__build_common_attributes(device_id)
        self.write_records(records, database_name, table_name, common_attributes)
    """


def __generate_write_records() -> str:
    """
    This function generates the method used to write records to Timestream.
    :return: The method used to write records to Timestream.
    """
    return """    def write_records(self, records: list, database_name: str, table_name: str, common_attributes=None):
        try:
            if not records or len(records) <= 0:
                raise ValueError("Empty records")

            if common_attributes is None:
                common_attributes = {}

            result = self.timestream_write.write_records(DatabaseName=database_name,
                                                         TableName=table_name,
                                                         Records=records,
                                                         CommonAttributes=common_attributes)

        except Exception as error:
            raise Exception(f"An error occurred while writing records to Timestream. {str(error)}")
    """


def __generate_build_records() -> str:
    """
    This function generates the method used to build records.
    :return: The method used to build records.
    """
    return """
    def __build_records(self, status_changes: [DeviceStatusChange]) -> [dict]:
        records = []
        for change in status_changes:
            value = change.new_value
            valueType = self.__get_value_timestream_type(value)
            records.append({
                'MeasureName': change.signal,
                'MeasureValue': str(value),
                'MeasureValueType': valueType
            })

        return records
    """


def __generate_build_common_attributes() -> str:
    """
    This function generates the method used to build common attributes.
    :return: The method used to build common attributes.
    """
    return """    def __build_common_attributes(self, device_id: str) -> [dict]:
        dimensions = [{'Name': 'device', 'Value': device_id}]

        return {
            "Dimensions": dimensions,
            "Time": str(int(time.time() * 1000))
        }
    """


def __generate_get_value_timestream_type() -> str:
    """
    This function generates the method used to get the value timestream type.
    :return: The method used to get the value timestream type.
    """
    return """    @staticmethod
    def __get_value_timestream_type(value):
        valueType = type(value)
        if valueType is str:
            return 'VARCHAR'
        elif valueType is bool:
            return 'BOOLEAN'
        elif valueType is int or valueType is float or valueType is Decimal:
            return 'DOUBLE'
        else:
            return None
    """