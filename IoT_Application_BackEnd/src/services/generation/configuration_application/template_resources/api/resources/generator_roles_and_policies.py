from services.generation.utility_methods import get_dynamo_data


def generate_roles_and_policies(json: dict) -> str:
    """
    This function generates the roles and policies of the api-related CloudFormation template.
    :param json: the json configuration.
    :return: the roles and policies of the api-related CloudFormation template.
    """
    return f"""
{__generate_role()}
{__generate_policy(json)}
    """


def __generate_role() -> str:
    """
    This function generates the role of the api-related CloudFormation template.
    :return: the role of the api-related CloudFormation template.
    """
    return """
  LambdaExecutionRoleGenerator:
    Type: AWS::IAM::Role
    Properties:
      Path: "/"
      RoleName: !Sub "${Project}-LambdaExecutionRoleGenerator"
      AssumeRolePolicyDocument: !Sub '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}'
      MaxSessionDuration: 3600
      ManagedPolicyArns:
        - 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
    """


def __generate_policy(json: dict) -> str:
    """
    This function generates the policy of the api-related CloudFormation template.
    :param json: the json configuration.
    :return: the policy of the api-related CloudFormation template.
    """

    dynamo_tables = get_dynamo_data(json)

    return f"""
  LambdaExecutionPolicyGenerator:
    Type: AWS::IAM::Policy
    Properties:
      PolicyName: !Sub "${{Project}}-LambdaExecutionPolicyGenerator"
      PolicyDocument:
        Version: 2012-10-17
        Statement:
          - Effect: Allow
            Action:
              - "dynamodb:PutItem"
              - "dynamodb:DeleteItem"
              - "dynamodb:Scan"
              - "dynamodb:Query"
              - "dynamodb:UpdateItem"
              - "dynamodb:GetItem"
            Resource:
{__generate_resource_policy(dynamo_tables)}
      Roles:
        - !Ref LambdaExecutionRoleGenerator
    """


def __generate_resource_policy(dynamo_tables: list) -> str:
    """
    This function generates the resource policy of the api-related CloudFormation template.
    :param dynamo_tables: the list of tables.
    :return: the resource policy of the api-related CloudFormation template.
    """
    return "".join(map(lambda resource: __generate_table_resource(resource), dynamo_tables))


def __generate_table_resource(table: dict) -> str:
    """
    This function generates the resource definition for a DynamoDB table.
    :param table: the table data.
    :return: the resource definition for a DynamoDB table.
    """
    return f"""              - !Sub "arn:aws:dynamodb:${{AWS::Region}}:${{AWS::AccountId}}:table/{table['tableName']}"
              - !Sub "arn:aws:dynamodb:${{AWS::Region}}:${{AWS::AccountId}}:table/{table['tableName']}/index/{table['GSI']['index_name']}" 
"""
