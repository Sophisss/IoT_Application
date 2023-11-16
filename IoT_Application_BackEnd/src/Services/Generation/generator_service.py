from Services.Generation.DAL.generator_lambda_service import generate_lambda_code
from Services.Generation.Templates.api.generate_lambda_template import generate_lambda_template
from Services.Generation.Templates.cognito.generate_cognito_template_service import generate_cognito_template


def generate_code(json: dict) -> dict:
    """
    This function generate the code.
    :param json: the json with the data.
    :return: the code generated.
    """
    codes_generated = {
        "cognito.yaml": generate_cognito_template(json['awsConfig']['authentication']['cognito']),
        "api.yaml": generate_lambda_template(json),
        "lambda.py": generate_lambda_code(json)}
    return codes_generated
