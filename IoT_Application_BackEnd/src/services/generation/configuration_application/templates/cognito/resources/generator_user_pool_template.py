def generate_user_pool(json: dict) -> str:
    """
    This function generates the user pool template.
    :param json: The json object containing the user pool information.
    :return: The user pool template.
    """
    return f"""
  {json["resource_name"]}:
    Type: AWS::Cognito::UserPool
    Properties: {__generate_user_pool_properties(json)}
    """


def __generate_user_pool_properties(json: dict) -> str:
    """
    This function generates the user pool properties.
    :param json: The json object containing the user pool information.
    :return: The user pool properties.
    """
    return f""" 
      UserPoolName: !Sub "${{Project}}-{json["UserPoolName"]}"
      Policies: {__generate_user_pool_policies(json['policy'])}
      LambdaConfig: {{}}
      AutoVerifiedAttributes:
        - "email"
      UsernameAttributes:
        - "email"
      UserPoolTags:
        Project: !Ref Project"""


def __generate_user_pool_policies(json: dict) -> str:
    """
    This function generates the user pool policies.
    :param json: The json object containing the user pool policies information.
    :return: The user pool policies.
    """
    return f"""
        PasswordPolicy: {__generate_user_pool_password_policy(json["PasswordPolicy"])}"""


def __generate_user_pool_password_policy(json: dict) -> str:
    """
    This function generates the user pool password policy.
    :param json: The json object containing the user pool password policy information.
    :return: The user pool password policy.
    """
    return f"""
          MinimumLength: {json["MinimumLength"]}
          RequireUppercase: {json["RequireUppercase"]}
          RequireLowercase: {json["RequireLowercase"]}
          RequireNumbers: {json["RequireNumbers"]}
          RequireSymbols: {json["RequireSymbols"]}
          TemporaryPasswordValidityDays: {json["TemporaryPasswordValidityDays"]}"""
