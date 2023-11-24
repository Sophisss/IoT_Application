from Services.Generation.utility_methods import generate_resource_name


def generate_lambda_template(json: dict) -> str:
    """
    This function generate the CloudFormation template for AWS Lambda function.
    :param json: JSON data containing Lambda function configuration.
    :return: the lambda-related CloudFormation template.
    """
    return "".join(map(lambda resource: __generate_lambda_resource(generate_resource_name(resource)), json))


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
     FunctionName: !Sub "${{Project}}-{resource_name}"
     CodeUri: ../src/
     Handler: lambda.lambda_handler_{resource_name}
     Role:
       Fn::ImportValue: !Sub "${{Project}}-LambdaExecutionRoleArn"
     Tags:
        Name: !Sub "${{Project}}-{resource_name}"
        """
