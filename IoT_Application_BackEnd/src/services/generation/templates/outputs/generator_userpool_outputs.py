def generate_user_pool_outputs() -> str:
    """
    This function generates the user pool outputs.
    :return: The user pool outputs.
    """
    return f"""{__generate_user_pool_id()}
{__generate_secret_id()}    
    """


def __generate_user_pool_id() -> str:
    """
    This function generates the user pool id output.
    :return: The user pool id output.
    """
    return """
  IoTApplicationUserPoolId:
    Description: IoT Application User Pool Id
    Value: !Ref IoTApplicationUserPool
    Export:
      Name: !Sub "${Project}-IoTApplicationUserPoolId" """


def __generate_secret_id() -> str:
    """
    This function generates the secret id output.
    :return: The secret id output.
    """
    return """
  ClientSecret:
    Description: IoT Application User Pool Client Secret
    Value: !GetAtt UserPoolWebClient.ClientSecret
    Export:
      Name: !Sub "${Project}-IoTApplicationUserPoolClientSecret"
    """
