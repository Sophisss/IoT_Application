def generate_identity_pool(json: dict) -> str:
    """
    This function generate the IdentityPool of the Cognito-related CloudFormation template.
    :param json: the JSON data.
    :return: the IdentityPool of the Cognito-related CloudFormation template.
    """
    return f"""
  {json["resource_name"]}:
    Type: AWS::Cognito::IdentityPool
    Properties: {generate_identity_pool_properties(json)}
    """


def generate_identity_pool_properties(json: dict) -> str:
    """
    This function generate the properties of the IdentityPool
    of the Cognito-related CloudFormation template.
    :param json: the JSON data.
    :return: the properties of the IdentityPool.
    """
    return f""" 
      IdentityPoolName: !Sub "${{Project}}-{json["IdentityPoolName"]}"
      AllowUnauthenticatedIdentities: false
      CognitoIdentityProviders:
        - ProviderName: !Sub "cognito-idp.${{AWS::Region}}.amazonaws.com/${{IoTApplicationUserPool}}"
      ServerSideTokenCheck: false"""
