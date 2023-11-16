def generate_api_template(json: dict) -> str:
    """
    This function generates the api-related CloudFormation template.
    :param json: the JSON data.
    :return: the api-related CloudFormation template.
    """
    return f"""{generate_resources(json['entities'] + json['links'])}
        """


def generate_resources(json: dict) -> str:
    """
    This function generate the resources of the api-related CloudFormation template.
    :param json: the JSON data.
    :return: the resources of the api-related CloudFormation template.
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


def generate_resource_name(resource):
    """
    This function generate the resource name.
    :param resource: The resource.
    :return: The resource name.
    """
    return resource.get("name") or f"{resource['first_entity']}{resource['second_entity']}"


def generate_properties_lambda(resource_name) -> str:
    """
    This function add the lambda function properties to the CloudFormation template.
    :param resource_name: the name of the resource.
    :return: the lambda function properties.
    """
    return f"""
      FunctionName: !Sub "${{Project}}-{resource_name}"
      CodeUri: src/
      Handler: api.lambda_handler_{resource_name}
      Role:   
        Fn::ImportValue: !Sub "${{Project}}-LambdaExecutionRoleArn"
      Tags:
        Name: !Sub "${{Project}}-{resource_name}"
    """

