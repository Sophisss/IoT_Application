from services.generation.utility_methods import get_timestream_data
from services.generation.configuration_application.template_resources.generator_header_template import \
    generate_header_template


def generate_telemetry_resources_template(json: dict) -> str:
    """
    This function generates the resources to monitor the changes in the device shadow and stores the data in Timestream.
    :param json: the json object.
    :return: the resources to monitor the changes in the device shadow and stores the data in Timestream.
    """
    return f"""{__generate_device_changes_resources(json)}
{__generate_lambda_role()}
{__generate_lambda_policy(json)}
{__generate_lambda_permission()}
{__generate_thing()}
    """


def __generate_device_changes_resources(json: dict) -> str:
    """
    This function generates the resources to monitor the changes in the device shadow and stores the data in Timestream.
    :param json: the json object.
    :return: the resources to monitor the changes in the device shadow and stores the data in Timestream.
    """

    topic = json['awsConfig']['iot'].get('topic')

    return f"""{__generate_lambda_mqtt()}
{__generate_rule_mqtt(topic)}
      """ if topic else \
        f"""{__generate_lambda_shadow_changes()}
{__generate_rule_shadow_changes()}
      """


def __generate_lambda_shadow_changes() -> str:
    """
    This function generates the lambda that monitors the changes in the device shadow and stores the data in Timestream.
    :return: the lambda that monitors the changes in the device shadow and stores the data in Timestream.
    """
    return """  DeviceStatusMonitoringShadow:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub "${Project}-DeviceStatusMonitoringShadow"
      Description:  Lambda che controlla i cambiamenti di stato dei dispositivi ed archivia i dati su Timestream
      CodeUri: ../src/
      Handler: iot_rules_app.monitor_device_status_shadow
      Role: !GetAtt DeviceStatusMonitoringLambdaRole.Arn
      Tags:
        Name: !Sub "${Project}-DeviceStatusMonitoringShadow"
    """


def __generate_lambda_mqtt() -> str:
    """
    This function generates the lambda that receives an mqtt message with the changes in the device status and stores the data in Timestream.
    :return: the lambda that receives an mqtt message with the changes in the device status and stores the data in Timestream.
    """
    return """  DeviceStatusMonitoring:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub "${Project}-DeviceStatusMonitoring"
      Description: Lambda che riceve un messaggio mqtt con i cambiamenti di stato dei dispositivi ed archivia i dati su Timestream
      CodeUri: ../src/
      Handler: iot_rules_app.monitor_device_status_mqtt
      Role: !GetAtt DeviceStatusMonitoringLambdaRole.Arn
      Tags:
        Name: !Sub "${Project}-DeviceStatusMonitoring"
    """


def __generate_lambda_role() -> str:
    """
    This function generates the role for the lambdas.
    :return: the role for the lambdas.
    """
    return """  DeviceStatusMonitoringLambdaRole:
    Type: AWS::IAM::Role
    Properties:
      Path: "/"
      RoleName: !Sub "${Project}-DeviceStatusMonitoringLambdaRole"
      AssumeRolePolicyDocument: !Sub '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}'
      MaxSessionDuration: 3600
      ManagedPolicyArns:
        - 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        """


def __generate_lambda_policy(json: dict) -> str:
    """
    This function generates the policy for the role of the lambdas.
    :param json: the json object.
    :return: the policy for the role of the lambdas.
    """
    database_name, table_name = get_timestream_data(json)

    return f"""  DeviceStatusMonitoringLambdaPolicy:
    Type: AWS::IAM::Policy
    Properties:
      PolicyName: !Sub "${{Project}}-DeviceStatusMonitoringLambdaPolicy"
      PolicyDocument:
        Version: 2012-10-17
        Statement:
          - Effect: Allow
            Action:
              - "timestream:DescribeEndpoints"
            Resource:
              - "*"
          - Effect: Allow
            Action:
              - "timestream:WriteRecords"
            Resource:
              - !Sub "arn:aws:timestream:${{AWS::Region}}:${{AWS::AccountId}}:database/{database_name}/table/{table_name}"
      Roles:
        - !Ref DeviceStatusMonitoringLambdaRole
    """


def __generate_rule_shadow_changes() -> str:
    """
    This function generates the IoT rule who intercepts device shadow changes and send them to a lambda.
    :return: the IoT rule who intercepts device shadow changes and send them to a lambda.
    """
    return """  STDeviceStatusMonitoringRule: # IoT Rule who intercepts device shadow changes and send them to a lambda
    Type: AWS::IoT::TopicRule
    Properties:
      RuleName: !Sub "${Project}_STDeviceStatusMonitoringRule"
      TopicRulePayload:
        RuleDisabled: false
        AwsIotSqlVersion: 2016-03-23
        Sql: !Sub "SELECT *, topic(3) AS thingName FROM '$aws/things/+/shadow/update/documents' WHERE current.state.reported <> previous.state.reported"
        Actions:
          - Lambda:
              FunctionArn: !GetAtt DeviceStatusMonitoringShadow.Arn
      Tags:
        - Key: Project
          Value: !Ref Project
        - Key: Name
          Value: !Sub "${Project}_STDeviceStatusMonitoringRule"
    """


def __generate_rule_mqtt(topic: str) -> str:
    """
    This function generates the IoT rule who intercepts mqtt messages and send them to a lambda.
    :topic: the topic to intercept.
    :return: the IoT rule who intercepts mqtt messages and send them to a lambda.
    """
    return f"""  DeviceStatusMonitoringRule:
    Type: AWS::IoT::TopicRule
    Properties:
      RuleName: !Sub "${{Project}}_DeviceStatusMonitoringRule"
      TopicRulePayload:
        RuleDisabled: false
        AwsIotSqlVersion: 2016-03-23
        Sql: "SELECT *, topic(2) AS thingName FROM '{topic}'"
        Actions:
          - Lambda:
              FunctionArn: !GetAtt DeviceStatusMonitoring.Arn
      Tags:
        - Key: Project
          Value: !Ref Project
        - Key: Name
          Value: !Sub "${{Project}}_DeviceStatusMonitoringRule"
    """


def __generate_lambda_permission() -> str:
    """
    This function generates the permission to invoke the lambda.
    :return: the permission to invoke the lambda.
    """
    return """  DeviceStatusMonitoringRuleInvokeLambdaPermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref DeviceStatusMonitoring
      Action: "lambda:InvokeFunction"
      Principal: "iot.amazonaws.com"
      SourceArn: !GetAtt DeviceStatusMonitoringRule.Arn
    """


def __generate_thing() -> str:
    """
    This function generates the IoT thing.
    :return: the IoT thing.
    """
    return """  IoThing:
    Type: AWS::IoT::Thing
    Properties:
      ThingName: !Sub "${Project}-IoTThing"
      AttributePayload:
        Attributes:
          Key: Environment
          Value: Test
    """
