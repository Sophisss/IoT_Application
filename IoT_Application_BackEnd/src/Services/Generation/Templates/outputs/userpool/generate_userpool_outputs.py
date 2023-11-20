def generate_user_pool_outputs():
    """
    This function generates the user pool outputs.
    :return: The user pool outputs.
    """
    return f"""{generate_user_pool_id()}
    """


def generate_user_pool_id():
    """
    This function generates the user pool id output.
    :return: The user pool id output.
    """
    return """
  IoTApplicationUserPoolId:
    Description: IoT Application User Pool Id
    Value: !Ref IoTApplicationUserPool
    Export:
      Name: !Sub "${Project}-IoTApplicationUserPoolId"
    """