from Services.Generation.DAL.DynamoClass.generate_dynamo_class import generate_dbmanager
from Services.Generation.DAL.Exception.generation_exception import generator_exception
from Services.Generation.DAL.generator.generation_in_one_file import generation_one_file
from Services.Generation.DAL.generator.generation_invoker import generator_invoker
from Services.Generation.Deployment_guide.generate_deployment_guide import generate_deployment_guide
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
        "src/graphql/schema.graphql": generate_graphql_schema(json),
        "src/graphql/invoker.js": generator_invoker(),
        "src/lambda.py": generation_one_file(json),
        "src/DynamoClass.py": generate_dbmanager(json),
        "src/ExceptionClasses.py": generator_exception(),
        "template/deployment_guide.md": generate_deployment_guide()}
    return codes_generated
