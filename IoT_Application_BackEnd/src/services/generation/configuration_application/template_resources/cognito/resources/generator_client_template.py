def generate_client() -> str:
    """
    This function generates the client template for the Cognito User Pool.
    :return: The client template for the Cognito User Pool.
    """
    return f"""
  UserPoolWebClient:
    Type: AWS::Cognito::UserPoolClient
    Properties: {__generate_client_properties()}
    """


def __generate_client_properties() -> str:
    """
    This function generates the client properties for the Cognito User Pool.
    :return: The client properties for the Cognito User Pool.
    """
    return f"""
      UserPoolId: !Ref IoTApplicationUserPool
      ClientName: "WebClient"
      RefreshTokenValidity: 365
      ExplicitAuthFlows: {__generate_explicit_auth_flows()}
      GenerateSecret: true
      CallbackURLs:
        - "devq://"
      LogoutURLs:
        - "devq://"
      AllowedOAuthFlows: {__generate_allowed_oauth_flows()}
      AllowedOAuthScopes: {__generate_allowed_oauth_scopes()}
      AllowedOAuthFlowsUserPoolClient: true
      IdTokenValidity: 60
      AccessTokenValidity: 60
      TokenValidityUnits: {__generate_token_validity_units()}
    """


def __generate_explicit_auth_flows() -> str:
    """
    This function generates the explicit auth flows for the Cognito User Pool.
    :return: The explicit auth flows for the Cognito User Pool.
    """
    return """
        - "ALLOW_CUSTOM_AUTH"
        - "ALLOW_REFRESH_TOKEN_AUTH"
        - "ALLOW_USER_PASSWORD_AUTH"
        - "ALLOW_USER_SRP_AUTH" """


def __generate_allowed_oauth_flows() -> str:
    """
    This function generates the allowed oauth flows for the Cognito User Pool.
    :return: The allowed oauth flows for the Cognito User Pool.
    """
    return """
        - "code" """


def __generate_allowed_oauth_scopes() -> str:
    """
    This function generates the allowed oauth scopes for the Cognito User Pool.
    :return: The allowed oauth scopes for the Cognito User Pool.
    """
    return """
        - "email"
        - "openid"
        - "profile" """


def __generate_token_validity_units() -> str:
    """
    This function generates the token validity units for the Cognito User Pool.
    :return: The token validity units for the Cognito User Pool.
    """
    return """
        AccessToken: "minutes"
        IdToken: "minutes"
        RefreshToken: "days" """