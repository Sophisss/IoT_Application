# Function that add the lambda functions to the CloudFormation template.
def add_lambda_template(json_data, template):
    add_lambda_resources(json_data["entities"], template)
    add_lambda_resources(json_data["links"], template)


# Function that update the lambda-related CloudFormation template with new resources.
def add_lambda_resources(resources, template):
    for resource in resources:
        resource_name = resource.get("name") or f"{resource['first_entity']}{resource['second_entity']}"
        template['Resources'][f'{resource_name}Handler'] = {
            "Type": "AWS::Serverless::Function",
            "Properties": add_properties_lambda_template(resource_name)
        }


# Function that add the lambda function properties to the CloudFormation template.
def add_properties_lambda_template(resource_name):
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

