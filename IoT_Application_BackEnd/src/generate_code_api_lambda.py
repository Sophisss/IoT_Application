from utility_methods import generate_resource_name


def add_lambda_template(json_data, template):
    """
    This function add the lambda functions to the CloudFormation template.
    :param json_data: the JSON data of the API.
    :param template: the CloudFormation template.
    """
    add_lambda_resources(json_data["entities"] + json_data["links"], template)


def add_lambda_resources(resources, template):
    """
    This function update the lambda-related CloudFormation template with new resources.
    :param resources: json data.
    :param template: the CloudFormation template.
    """
    for resource in resources:
        resource_name = generate_resource_name(resource)
        template['Resources'][f'{resource_name}Handler'] = {
            "Type": "AWS::Serverless::Function",
            "Properties": add_properties_lambda_template(resource_name)
        }


def add_properties_lambda_template(resource_name):
    """
    This function add the lambda function properties to the CloudFormation template.
    :param resource_name: the name of the resource.
    :return: the lambda function properties.
    """
    return {
        "FunctionName": {"Fn::Sub": "${Project}-" + resource_name + "Handler"},
        "CodeUri": "src/",  # TODO rivedi
        "Handler": f"api.lambda_handler_{resource_name}",
        "Role": {"Fn::ImportValue": {
            "Fn::Sub": "${Project}-LambdaExecutionRoleArn"
        }},
        "Tags": {
            "Name": {"Fn::Sub": "${Project}-" + resource_name + "Handler"}
        }
    }

