from Services.Generation.utility_methods import generate_resource_name


def generate_graphql_template(json: dict) -> str:
    return f"""
  GraphQLAPI:
    Type: AWS::Serverless::GraphQLApi
    Properties: {generate_properties(json)}
    """


def generate_properties(resources: dict):
    properties = generate_properties_graphql()
    datasource = generate_datasource()
    functions = generate_functions()
    resolvers = generate_resolver()
    query = add_query()
    mutation = add_mutation()
    return add_properties_graphql_api_template(resources, datasource, functions, resolvers, properties, query, mutation)


def add_properties_graphql_api_template(resources: dict, datasource: str, functions: str, resolvers: str, properties: str, query, mutation) -> str:
    returns = []
    for resource in resources:
        resource_name = generate_resource_name(resource)
        datasource += add_datasource(resource_name)
        functions += add_functions(resource_name)
        query, mutation = add_resolver(resource, resource_name, query, mutation)
    resolvers += query + mutation
    returns.append(properties + datasource + functions + resolvers)

    return "".join(returns)


def generate_properties_graphql() -> str:
    return """
      SchemaUri: src/schema.graphql
      Auth:
        Type: API_KEY"""


def generate_datasource():
    return """
      DataSources:
        Lambda:"""



def add_datasource(resource_name: str) -> str:
    return f"""
          Lambda{resource_name}:
            Name: !Sub "${{Project}}_Lambda{resource_name}"
            Description: Lambda DataSource
            FunctionArn: !GetAtt {resource_name}Handler.Arn"""


def generate_functions():
    return """
      Functions:"""


def add_functions(resource_name: str) -> str:
    return f"""
        lambdaInvoker{resource_name}:
          CodeUri: src/invoker.js
          DataSource: Lambda{resource_name}
          Description: Lambda invoker function
          Runtime:
            Name: APPSYNC_JS
            Version: 1.0.0"""


def generate_resolver() -> str:
    return """
      Resolvers:"""


def add_resolver(resource: dict, resource_name: str, query: str, mutation: str) -> tuple[str, str]:
    for api in resource["API"]:
        if api["type"] == "GET":
            query += add_body_resolver(api["name"], resource_name)
        else:
            mutation += add_body_resolver(api["name"], resource_name)

    return query, mutation


def add_query() -> str:
    return """
        Query:"""


def add_mutation() -> str:
    return """
        Mutation:"""


def add_body_resolver(method: str, resource_name: str) -> str:
    return f"""
          {method}:
            Pipeline:
              - lambdaInvoker{resource_name}
            Runtime:
              Name: APPSYNC_JS
              Version: 1.0.0"""
