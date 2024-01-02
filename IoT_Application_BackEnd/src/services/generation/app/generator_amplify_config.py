def generate_amplify_configuration() -> str:
    """
    This method generates the amplify configuration file.
    :return: The amplify configuration.
    """
    return """{
  "api": {
    "plugins": {
      "awsAPIPlugin": {
        "api": {
          "_comment": "Add your pool GraphQL endpoint and delete this line",
          "endpoint": "",
          "authorizationType": "AMAZON_COGNITO_USER_POOLS",
          "endpointType": "GraphQL",
          "region": "eu-central-1"
        }
      }
    }
  },
  "auth": {
    "plugins": {
      "awsCognitoAuthPlugin": {
        "IdentityManager": {
          "Default": {}
        },
        "CredentialsProvider": {
          "CognitoIdentity": {
            "Default": {}
          }
        },
        "CognitoUserPool": {
          "Default": {
            "_comment": "Add your pool id, client id, secret and delete this line",
            "PoolId": "",
            "AppClientId": "",
            "AppClientSecret": "",
            "Region": "eu-central-1"
          }
        },
        "Auth": {
          "Default": {
            "authenticationFlowType": "USER_SRP_AUTH",
            "OAuth": {
              "_comment": "Add your client id, secret, redirect and delete this line",
              "AppClientId": "",
              "AppClientSecret": "",
              "SignInRedirectURI": "",
              "SignOutRedirectURI": "",
              "Scopes": [
                "email",
                "openid",
                "profile",
                "aws.cognito.signin.user.admin"
              ]
            }
          }
        }
      }
    }
  }
} """