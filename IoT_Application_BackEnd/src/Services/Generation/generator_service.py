from Services.Generation.DAL.generator.generation_dbmanager import generator_dbmanager
from Services.Generation.DAL.generator.generation_exception import generator_exception
from Services.Generation.DAL.generator.generation_in_one_file import generation_one_file
from Services.Generation.DAL.generator.generation_invoker import generator_invoker
from Services.Generation.Deployment_guide.generate_deployment_guide import generate_deployment_guide
from Services.Generation.Schema_GraphQL.generator_schema import generate_graphql_schema
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
        "src/invoker.js": generator_invoker(),
        "src/lambda.py": generation_one_file(json),
        "src/DynamoClass.py": generator_dbmanager(),
        "src/ExceptionClasses.py": generator_exception(),
        "template/deployment_guide.md": generate_deployment_guide()}
    return codes_generated
