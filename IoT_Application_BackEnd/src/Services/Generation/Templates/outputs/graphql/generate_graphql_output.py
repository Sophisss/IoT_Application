def generate_graphql_outputs():
    """
    This function generates the GraphQLAPI outputs.
    :return: The GraphQLAPI outputs.
    """
    return f"""{generate_graphql_endpoint()}"""


def generate_graphql_endpoint():
    """
    This function generates the GraphQLAPIEndpoint output.
    :return: The GraphQLAPIEndpoint output.
    """
    return """
  GraphQLAPIEndpoint:
    Description: GraphQLAPIEndpoint
    Value: !GetAtt GraphQLAPI.GraphQLUrl
    Export:
      Name: !Sub "${Project}-GraphQLAPIEndpoint" """
