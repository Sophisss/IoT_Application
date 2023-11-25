def generate_graphql_outputs() -> str:
    """
    This function generates the GraphQLAPI outputs.
    :return: The GraphQLAPI outputs.
    """
    return f"""{__generate_graphql_endpoint()}"""


def __generate_graphql_endpoint() -> str:
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
