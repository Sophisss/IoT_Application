from Services.Generation.DAL.generator_lambda_service import generate_lambda_code
from Services.Generation.Schema_graphQL.generator_schema import generate_graphql_schema
from Services.Generation.Templates.api.generate_api_template import generate_api_template
from Services.Generation.Templates.cognito.generate_cognito_template_service import generate_cognito_template


def generate_code(json: dict) -> dict:
    """
    This function generate the code.
    :param json: the json with the data.
    :return: the code generated.
    """
    codes_generated = {
        "template/cognito.yaml": generate_cognito_template(json['awsConfig']['authentication']['cognito']),
        "template/api.yaml": generate_api_template(json),
        "src/schema.graphql": generate_graphql_schema(json),
        "src/lambda.py": generate_lambda_code(json)}
    return codes_generated
