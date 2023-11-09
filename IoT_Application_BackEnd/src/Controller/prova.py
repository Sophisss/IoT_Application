import json
from ruamel.yaml import YAML


def read_json():
    with open('../cognito.json', 'r') as opened_file:
        source_file = json.loads(opened_file.read())
    return source_file


def add_to_resources_template_cognito(yaml):
    # Carica il documento YAML esistente
    with open('../../templates/prova.yaml', 'r') as existing_template:
        template = yaml.load(existing_template)

    # Aggiungi il nuovo elemento alla sezione "Resources"
    if 'Resources' not in template:
        template['Resources'] = {}

    json_data = read_json()
    add_user_pool(yaml, json_data, template)
    add_identity_pool(yaml, json_data, template)


def add_user_pool(yaml, json_data, template):
    user_pool_name = json_data["UserPool"]["resource_name"]
    password_policy = json_data["UserPool"]["policy"]["PasswordPolicy"]
    new_resource = {
        f"{user_pool_name}": {
            "Type": "AWS::Cognito::UserPool",
            "Properties": {
                "UserPoolName": json_data["UserPool"]["UserPoolName"],
                "Policies": {
                    "PasswordPolicy": {
                        "MinimumLength": password_policy["MinimumLength"],
                        "RequireUppercase": password_policy["RequireUppercase"],
                        "RequireLowercase": password_policy["RequireLowercase"],
                        "RequireNumbers": password_policy["RequireNumbers"],
                        "RequireSymbols": password_policy["RequireSymbols"],
                        "TemporaryPasswordValidityDays": password_policy["TemporaryPasswordValidityDays"]
                    }
                },
                "LambdaConfig": {},
                "AutoVerifiedAttributes": ["email"],
                "UsernameAttributes": ["email"],
                "UserpoolTags": {
                    "Project": "!Ref Project"
                }
            }
        }
    }
    template['Resources'].update(new_resource)
    with open('../../templates/prova.yaml', 'w') as updated_template:
        yaml.dump(template, updated_template)


def add_identity_pool(yaml, json_data, template):
    identity_pool_name = json_data["IdentityPool"]["resource_name"]
    new_resource = {
        f"{identity_pool_name}": {
            "Type": "AWS::Cognito::IdentityPool",
            "Properties": {
                "IdentityPoolName": json_data["IdentityPool"]["IdentityPoolName"],
                "AllowUnauthenticatedIdentities": False,
                "CognitoIdentityProviders": [
                    {
                        "ProviderName": "!Ref UserPool"
                    }
                ],
                "ServerSideTokenCheck": False
            }
        }
    }
    template['Resources'].update(new_resource)
    with open('../../templates/prova.yaml', 'w') as updated_template:
        yaml.dump(template, updated_template)


def generate_templates():
    yaml = YAML()
    add_to_resources_template_cognito(yaml)


generate_templates()
