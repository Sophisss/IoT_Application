from services.generation.utility_methods import generate_resource_name


def generate_lambda_template(resources: list) -> str:
    """
    This function generate the CloudFormation template for AWS Lambda function.
    :param resources: the list of resources.
    :return: the lambda-related CloudFormation template.
    """
    return "".join(map(lambda resource: __generate_lambda_resource(generate_resource_name(resource)), resources))


def __generate_lambda_resource(resource_name: str) -> str:
    """
    This function generates the resource definition for a Lambda function.
    :param resource_name: the name of the resource.
    :return: the resource definition for a Lambda function.
    """
    return f"""
  {resource_name}Handler:
    Type: AWS::Serverless::Function
    Properties: {__generate_lambda_properties(resource_name)}
          """


def __generate_lambda_properties(resource_name: str) -> str:
    """
    This function generate properties for a Lambda function.
    :param resource_name: the name of the resource.
    :return: properties for a Lambda function.
    """
    return f"""
     FunctionName: !Sub "${{Project}}-{resource_name}Handler"
     CodeUri: ../src/
     Handler: lambda_{resource_name.lower()}.lambda_handler_{resource_name.lower()}
     Role:
       !GetAtt LambdaExecutionRoleGenerator.Arn
     Tags:
        Name: !Sub "${{Project}}-{resource_name}Handler"
        """
