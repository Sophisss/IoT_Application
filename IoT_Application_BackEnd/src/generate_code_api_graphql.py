from utility_methods import generate_resource_name


def add_graphql_api_template(json_data, template):
    """
    This function add the graphql api to the CloudFormation template.
    :param json_data: The json data of the api.
    :param template: The CloudFormation template.
    """
    entities_and_links = json_data["entities"] + json_data["links"]
    template['Resources']['GraphQLAPI'] = {
        "Type": "AWS::Serverless::GraphQLApi",
        "Properties": add_properties_graphql_api_template(entities_and_links)
    }


def generate_graphql_api_properties():
    """
    This function generate the properties of the graphql api.
    :return: The properties of the graphql api.
    """
    return {
        "SchemaUri": "...",  # TODO add schema uri
        "Auth": {
            "Type": "APY_KEY"  # TODO IAM
        },
        "DataSources": {},
        "Functions": {},
        "Resolvers": {'Query': {}, 'Mutation': {}}
    }


def add_properties_graphql_api_template(resources):
    """
    This function add the properties of the graphql api to the CloudFormation template.
    :param resources: The resources.
    :return: The properties of the graphql api.
    """
    api_templates = generate_graphql_api_properties()
    for resource in resources:
        resource_name = generate_resource_name(resource)
        add_data_source(api_templates['DataSources'], resource_name)
        add_function(api_templates['Functions'], resource_name)
        add_resolver(api_templates['Resolvers'], resource, resource_name)

    return api_templates


def add_data_source(data_sources, resource_name):
    """
    This function add the graphql api data source to the CloudFormation template.
    :param data_sources: The data sources.
    :param resource_name: The resource name.
    """
    data_source_name = f'Lambda{resource_name}'
    data_sources[data_source_name] = {
        "name": {"Fn::Sub": "${Project}_" + data_source_name},
        "description": "Lambda DataSource",
        "FunctionArn": {"Fn::GetAtt": [f'{resource_name}Handler', "Arn"]}
    }


def add_function(functions, resource_name):
    """
    This function add the graphql api function to the CloudFormation template.
    :param functions: The functions.
    :param resource_name: The resource name.
    """
    function_name = f'lambdaInvoker{resource_name}'
    functions[function_name] = {
        "CodeUri": "...",  # TODO add code uri
        "DataSource": f'Lambda{resource_name}',
        "Description": "Lambda invoker function",
        "Runtime": {
            "Name": "APPSYNC_JS",
            "Version": "1.0.0"
        }
    }


def add_resolver(resolvers, resource, resource_name):
    """
    This function add the graphql api resolver to the CloudFormation template.
    :param resolvers: The resolvers.
    :param resource: The resource.
    :param resource_name: The resource name.
    """
    for api in resource["API"]:
        operation_type = 'Query' if api["type"] == 'GET' else 'Mutation'
        resolvers[operation_type][api["name"]] = generate_resolvers(resource_name)


def generate_resolvers(resource_name):
    """
    This function generate the resolvers for the graphql api.
    :param resource_name: The name of the resource.
    :return: The resolvers.
    """
    return {
        "Runtime": {
            "Name": "APPSYNC_JS",
            "Version": "1.0.0"
        },
        "Pipeline": [
            "lambdaInvoker" + resource_name
        ]
    }