def generate_role_template():
    """
    This function generates the role template for the cognito service.
    :return: Returns the role template for the cognito service.
    """
    return f"""
    {generate_identity_role()}"""


def generate_identity_role():
    """
    This function generates the identity role for the cognito service.
    :return: Returns the identity role for the cognito service.
    """
    return """
  SHIdentityPoolRoleAttachment:
    Type: AWS::Cognito::IdentityPoolRoleAttachment
    Properties:
      IdentityPoolId: !Ref IoTApplicationIdentityPool
      Roles:
        authenticated: !GetAtt CognitoAuthenticatedRole.Arn
        unauthenticated: !GetAtt CognitoUnauthenticatedRole.Arn"""