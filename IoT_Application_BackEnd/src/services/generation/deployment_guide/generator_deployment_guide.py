def generate_deployment_guide() -> str:
    """
    This function generates the deployment guide for the project.
    :return: The deployment guide for the project.
    """
    return f"""
{__generate_deployment_introduction()}
{__generate_deployment_guide_api_template()}
{__generate_deployment_guide_cognito_template()}
    """


def __generate_deployment_introduction() -> str:
    """
    This function generates the introduction for the deployment guide.
    :return: The introduction for the deployment guide.
    """
    return """
# DEPLOYMENT GUIDE

This guide will help you deploy the project to AWS.
    """


def __generate_deployment_guide_api_template() -> str:
    """
    This function generates the deployment guide for the api template.
    :return: The deployment guide for the api template.
    """
    return """
### Api template deployment

- sam build --template-file api.yaml 
- sam deploy --stack-name devq-iot-platform-graphql --template-file .aws-sam/build/template.yaml --parameter-overrides Project=IoT_Platform  --s3-bucket devq.iot.iot-platform  --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND
    """


def __generate_deployment_guide_cognito_template() -> str:
    """
    This function generates the deployment guide for the cognito template.
    :return: The deployment guide for the cognito template.
    """
    return """
### Cognito template deployment

- sam build --template-file cognito.yaml
- sam deploy --stack-name devq-iot-platform-cognito --template-file .aws-sam/build/template.yaml --parameter-overrides Project=IoT_Platform  --s3-bucket devq.iot.iot-platform  --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND
    """
