from services.generation.configuration_application.template_resources.generator_header_template import \
    generate_header_template
from services.generation.utility_methods import get_timestream_data


def generate_timestream_template(json: dict) -> str:
    """
    This function generates the TimeStream database and table for the IoT platform.
    :param json: The JSON configuration.
    :return: The TimeStream database and table for the IoT platform.
    """
    database_name, table_name = get_timestream_data(json)

    return f"""{__generate_timestream_database(database_name)}
{__generate_timestream_table(table_name, database_name)}
    """


def __generate_timestream_database(database_name: str) -> str:
    """
    This function generates the TimeStream database for the IoT platform.
    :param database_name: The name of the database.
    :return: The TimeStream database for the IoT platform.
    """
    return f"""  IoTPlatform{database_name}:
    Type: AWS::Timestream::Database
    Properties:
      DatabaseName: {database_name}
      Tags:
        - Key: Project
          Value: !Ref Project
        - Key: Name
          Value: {database_name}
    """


def __generate_timestream_table(table_name: str, database_name: str) -> str:
    """
    This function generates the TimeStream table for the IoT platform.
    :param table_name: The name of the table.
    :param database_name: The name of the database.
    :return: The TimeStream table for the IoT platform.
    """
    return f"""  
  IoTPlatformTimeStream{table_name}:
    Type: AWS::Timestream::Table
    Properties:
      DatabaseName: !Ref IoTPlatform{database_name}
      TableName: {table_name}
      RetentionProperties:
        MemoryStoreRetentionPeriodInHours: "1"
        MagneticStoreRetentionPeriodInDays: "1825"
      MagneticStoreWriteProperties:
        EnableMagneticStoreWrites: true
      Tags:
        - Key: Project
          Value: !Ref Project
        - Key: Name
          Value: {table_name}
    """
