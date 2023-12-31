def generate_header_template() -> str:
    """
    This function generate the header of the CloudFormation template.
    :return: the header of the CloudFormation template.
    """
    return f"""AWSTemplateFormatVersion: "2010-09-09"
Transform: AWS::Serverless-2016-10-31
Description: AWS CloudFormation Template

Parameters: {__add_parameters_template()}
Globals: {__add_globals_template()}
    """


def __add_parameters_template() -> str:
    """
    This function add the parameters to the CloudFormation template.
    :return: Parameters.
    """
    return """
  Project:
    Type: String
    Description: Project name
    """


def __add_globals_template() -> str:
    """
    This function add the globals to the CloudFormation template.
    :return: Globals.
    """
    return """
  Function:
    Timeout: 10
    Runtime: python3.11
    CodeUri: ../src/
    MemorySize: 256
    Environment:
      Variables:
        AWS_ACCOUNT_ID: !Ref AWS::AccountId
        DYNAMO_REGION: !Ref AWS::Region
    """