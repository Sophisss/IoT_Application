def generate_user_pool(json):
    return f"""UserPool:
    Type: AWS::Cognito::UserPool
    Properties: {generate_user_pool_properties(json)}
"""


def generate_user_pool_properties(json):
    return f"""UserPoolName: {json["UserPool"]["UserPoolName"]}
    Policies: {generate_user_pool_policies(json)}
    LambdaConfig: 
    AutoVerifiedAttributes: ["email"]
    UsernameAttributes: ["email"]
    UserpoolTags:
        Project: !Ref Project
    """


def generate_user_pool_policies(json):
    pass
