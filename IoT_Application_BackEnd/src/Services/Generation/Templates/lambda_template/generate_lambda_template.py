from Services.Generation.utility_methods import generate_resource_name


def generate_lambda_template(json: dict) -> str:
    """
    This function generates the lambda-related CloudFormation template.
    :param json: the JSON data.
    :return: the lambda-related CloudFormation template.
    """
    returns = []
    for resource in json:
        resource_name = generate_resource_name(resource)
        new_resource = f"""
  {resource_name}Handler:
    Type: AWS::Serverless::Function
    Properties: {generate_properties_lambda(resource_name)}
          """
        returns.append(new_resource)
    return "".join(returns)


def generate_properties_lambda(resource_name: str) -> str:
    """
    This function add the lambda function properties to the CloudFormation template.
    :param resource_name: the name of the resource.
    :return: the lambda function properties.
    """
    return f"""
     FunctionName: !Sub "${{Project}}-{resource_name}"
     CodeUri: ../src/
     Handler: lambda.lambda_handler_{resource_name}
     Role: !GetAtt LambdaExecutionRole.Arn
     Tags:
        Name: !Sub "${{Project}}-{resource_name}"
        """
