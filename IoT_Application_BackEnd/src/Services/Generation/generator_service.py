from Services.Generation.DAL.DynamoClass.generate_dynamo_class import generate_dbmanager
from Services.Generation.DAL.Exception.generation_exception import generator_exception
from Services.Generation.DAL.Model.generator_model_entity import generate_model_entity
from Services.Generation.DAL.Model.generator_model_link import generate_model_link
from Services.Generation.DAL.generator.generation_in_one_file import generation_one_file
from Services.Generation.Deployment_guide.generate_deployment_guide import generate_deployment_guide
from Services.Generation.GraphQL_resources.generate_invoker import generator_invoker
from Services.Generation.GraphQL_resources.generate_schema_graphql import generate_graphql_schema
from Services.Generation.Templates.api.generate_api_template import generate_api_template
from Services.Generation.Templates.cognito.generate_cognito_template_service import generate_cognito_template
from Services.Generation.utility_methods import generate_resource_name


def generate_code(json: dict) -> dict:
    """
    This function generate the code.
    :param json: the json containing the data.
    :return: the code generated.
    """
    code_generated = {}
    __generate_template_code(code_generated, json)
    __generate_entity_model(code_generated, json)
    __generate_link_model(code_generated, json)
    __generate_graphql_code(code_generated, json)
    __generate_dal_code(code_generated, json)
    __generate_deployment_guide(code_generated)
    return code_generated


def __generate_template_code(codes_generated: dict, json: dict):
    """
    This method generate the code for the templates.
    :param codes_generated: the code that will be generated.
    :param json: the json with the data.
    """
    codes_generated['code_generated/template/cognito.yaml'] = generate_cognito_template(json['awsConfig']['authentication']['cognito'])
    codes_generated['code_generated/template/api.yaml'] = generate_api_template(json)


def __generate_entity_model(codes_generated: dict, json: dict):
    """
    This method generate the code for the model entity.
    :param codes_generated: the code that will be generated.
    :param json: the json with the data.
    """
    for entity in json['entities']:
        entity_name = generate_resource_name(entity)
        codes_generated[f'code_generated/src/model/{entity_name}.py'] = generate_model_entity(entity_name, entity['fields'])


def __generate_link_model(codes_generated: dict, json: dict):
    """
    This method generate the code for the model link.
    :param codes_generated: the code that will be generated.
    :param json: the json with the data.
    """
    for link in json['links']:
        link_name = generate_resource_name(link)
        codes_generated[f'code_generated/src/model/{link_name}.py'] = generate_model_link(link, json)


def __generate_graphql_code(codes_generated: dict, json: dict):
    """
    This method generate the code for the graphql resources.
    :param codes_generated: the code that will be generated.
    :param json: the json with the data.
    """
    codes_generated['code_generated/src/graphql/schema.graphql'] = generate_graphql_schema(json)
    codes_generated['code_generated/src/graphql/invoker.js'] = generator_invoker()


def __generate_dal_code(codes_generated: dict, json: dict):
    """
    This method generate the code for the dal resources.
    :param codes_generated: the code that will be generated.
    :param json: the json with the data.
    """
    codes_generated['code_generated/src/DynamoClass.py'] = generate_dbmanager(json)
    codes_generated['code_generated/src/ExceptionClass.py'] = generator_exception()
    codes_generated['code_generated/src/lambda.py'] = generation_one_file(json)


def __generate_deployment_guide(codes_generated: dict):
    """
    This method generate the code for the deployment guide.
    :param codes_generated: the code that will be generated.
    """
    codes_generated['code_generated/template/guide/deployment_guide.md'] = generate_deployment_guide()
