# Function that add the graphql api to the CloudFormation template.
def add_graphql_api_template(json_data, template):
    template['Resources']['GraphQLAPI'] = {
        "Type": "AWS::Serverless::GraphQLApi",
        "Properties": add_properties_graphql_api_template(json_data)
    }


# Function that add the graphql api properties to the CloudFormation template.
def add_properties_graphql_api_template(resources):
    return {
        "Auth": {
            "Type": "APY_KEY"  # TODO IAM
        },
        "DataSources": {
            "Lambda": add_data_sources(resources["entities"] + resources["links"])
        },
        "Functions": add_functions(resources["entities"] + resources["links"]),
        "Resolvers": add_resolvers(resources["entities"] + resources["links"]),
    }


# Function that add the graphql api data source to the CloudFormation template.
def add_data_sources(resources):
    data_sources = {}
    for resource in resources:
        resource_name = resource.get("name") or f"{resource['first_entity']}{resource['second_entity']}"
        name = f'Lambda{resource_name}'
        data_sources[name] = {
            "name": {"Fn::Sub": "${Project}_" + name},
            "description": "Lambda DataSource",
            "FunctionArn": {"Fn::GetAtt": [f'{resource_name}Handler', "Arn"]},
        }
    return data_sources


# Function that add the graphql api functions to the CloudFormation template.
def add_functions(resources):
    functions = {}
    for resource in resources:
        resource_name = resource.get("name") or f"{resource['first_entity']}{resource['second_entity']}"
        name = f'lambdaInvoker{resource_name}'
        functions[name] = {
            "CodeUri": "...",
            "DataSource": f'Lambda{resource_name}',
            "Description": "Lambda invoker function",
            "Runtime": {
                "Name": "APPSYNC_JS",
                "Version": "1.0.0"
            }
        }
    return functions
