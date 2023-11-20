from Services.Generation.utility_methods import generate_resource_name


def generate_graphql_template(json: dict) -> str:
    """
    This function generates the GraphQL API template.
    :param json: The JSON file containing the API information.
    :return: The GraphQL API template.
    """
    return f"""
  GraphQLAPI:
    Type: AWS::Serverless::GraphQLApi
    Properties: {add_properties_graphql_api_template(json)}
    """


def add_properties_graphql_api_template(resources: dict) -> str:
    """
    This function adds the properties to the GraphQL API template.
    :param resources: The resources to add to the GraphQL API template.
    :return: The properties for the GraphQL API template.
    """
    properties, datasource, functions, resolvers, query, mutation = generate_properties()

    returns = []
    for resource in resources:
        resource_name = generate_resource_name(resource)
        datasource += add_datasource(resource_name)
        functions += add_functions(resource_name)
        query, mutation = add_resolver(resource, resource_name, query, mutation)
    resolvers += query + mutation
    returns.append(properties + datasource + functions + resolvers)

    return "".join(returns)


def generate_properties() -> tuple[str, str, str, str, str, str]:
    """
    This function generates the properties for the GraphQL API template.
    :return: The properties for the GraphQL API template.
    """
    properties = generate_properties_graphql()
    datasource = generate_datasource()
    functions = generate_functions()
    resolvers = generate_resolver()
    query = add_query()
    mutation = add_mutation()
    return properties, datasource, functions, resolvers, query, mutation


def generate_properties_graphql() -> str:
    """
    This function generates the properties for the GraphQL API template.
    :return: The properties for the GraphQL API template.
    """
    return f"""
      SchemaUri: ../src/schema.graphql
      Auth:
        Type: AMAZON_COGNITO_USER_POOLS
        UserPool: {generate_user_pool()}"""


def generate_user_pool() -> str:
    """
    This function generates the user pool for the GraphQL API template.
    :return: The user pool for the GraphQL API template.
    """
    return """
          AwsRegion: !Ref AWS::Region
          DefaultAction: ALLOW
          UserPoolId: 
            Fn::ImportValue: !Sub "${Project}-IoTApplicationUserPoolId" """


def generate_datasource():
    """
    This function generates the data sources for the GraphQL API template.
    :return: The data sources for the GraphQL API template.
    """
    return """
      DataSources:
        Lambda:"""


def add_datasource(resource_name: str) -> str:
    """
    This function adds a data source to the GraphQL API template.
    :param resource_name: The name of the resource.
    :return: The data source for the GraphQL API template.
    """
    return f"""
          Lambda{resource_name}:
            Name: !Sub "${{Project}}_Lambda{resource_name}"
            Description: Lambda DataSource
            FunctionArn: !GetAtt {resource_name}Handler.Arn"""


def generate_functions():
    """
    This function generates the functions for the GraphQL API template.
    :return: The functions for the GraphQL API template.
    """
    return """
      Functions:"""


def add_functions(resource_name: str) -> str:
    """
    This function adds a function to the GraphQL API template.
    :param resource_name: The name of the resource.
    :return: The function for the GraphQL API template.
    """
    return f"""
        lambdaInvoker{resource_name}:
          CodeUri: ../src/invoker.js
          DataSource: Lambda{resource_name}
          Description: Lambda invoker function
          Runtime:
            Name: APPSYNC_JS
            Version: 1.0.0"""


def generate_resolver() -> str:
    """
    This function generates the resolvers for the GraphQL API template.
    :return: The resolvers for the GraphQL API template.
    """
    return """
      Resolvers:"""


def add_resolver(resource: dict, resource_name: str, query: str, mutation: str) -> tuple[str, str]:
    """
    This function adds a resolver to the GraphQL API template.
    :param resource: The resource to add to the GraphQL API template.
    :param resource_name: The name of the resource.
    :param query: The query for the GraphQL API template.
    :param mutation: The mutation for the GraphQL API template.
    :return: The query and mutation for the GraphQL API template.
    """
    for api in resource["API"]:
        if api["type"] == "GET" or api["type"] == "GET_ALL":
            query += add_body_resolver(api["name"], resource_name)
        else:
            mutation += add_body_resolver(api["name"], resource_name)

    return query, mutation


def add_query() -> str:
    """
    This function adds a query to the GraphQL API template.
    :return: The query for the GraphQL API template.
    """
    return """
        Query:"""


def add_mutation() -> str:
    """
    This function adds a mutation to the GraphQL API template.
    :return: The mutation for the GraphQL API template.
    """
    return """
        Mutation:"""


def add_body_resolver(method: str, resource_name: str) -> str:
    """
    This function adds a body resolver to the GraphQL API template.
    :param method: The method to add to the GraphQL API template.
    :param resource_name: The name of the resource.
    :return: The body resolver for the GraphQL API template.
    """
    return f"""
          {method}:
            Pipeline:
              - lambdaInvoker{resource_name}
            Runtime:
              Name: APPSYNC_JS
              Version: 1.0.0"""
