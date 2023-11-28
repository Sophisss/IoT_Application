from services.generation.dal.dynamo_manager.configuration.generator_configuration_class import generate_configuration_class
from services.generation.dal.dynamo_manager.generator_dynamo_class import generate_dbmanager
from services.generation.dal.dynamo_manager.utility.generate_utility_functions import generate_utility_functions
from services.generation.dal.event.generator_event_class import generate_event_class
from services.generation.dal.event.generator_event_parse import generate_event_parse
from services.generation.dal.exception.generation_exception import generator_exception
from services.generation.dal.model.generator_model_entity import generate_model_entity
from services.generation.dal.model.generator_model_link import generate_model_link
from services.generation.dal.lambda_functions.generation_in_one_file import generation_one_file
from services.generation.deployment_guide.generate_deployment_guide import generate_deployment_guide
from services.generation.graphql_resources.generate_invoker import generator_invoker
from services.generation.graphql_resources.generate_schema_graphql import generate_graphql_schema
from services.generation.requirements.generator_requirements import generate_requirements
from services.generation.templates.api.generate_api_template import generate_api_template
from services.generation.templates.cognito.generate_cognito_template_service import generate_cognito_template
from services.generation.utility_methods import generate_resource_name


def generate_code(json: dict) -> dict:
    """
    This function generate the code.
    :param json: the json containing the data.
    :return: the code generated.
    """
    code_generated = {}
    __generate_templates(code_generated, json)
    __generate_deployment_guide(code_generated)
    __generate_requirements(code_generated)
    __generate_graphql_resources(code_generated, json)
    __generate_dal_resources(code_generated, json)
    return code_generated


def __generate_templates(codes_generated: dict, json: dict):
    """
    This method generate the code for the templates.
    :param codes_generated: the code that will be generated.
    :param json: the json with the data.
    """
    codes_generated['code_generated/template/cognito.yaml'] = generate_cognito_template(
        json['awsConfig']['authentication']['cognito'])
    codes_generated['code_generated/template/api.yaml'] = generate_api_template(json)


def __generate_deployment_guide(codes_generated: dict):
    """
    This method generate the code for the deployment guide.
    :param codes_generated: the code that will be generated.
    """
    codes_generated['code_generated/template/guide/deployment_guide.md'] = generate_deployment_guide()


def __generate_requirements(codes_generated: dict):
    """
    This method generate the code for the requirements.
    :param codes_generated: the code that will be generated.
    """
    codes_generated['code_generated/src/requirements.txt'] = generate_requirements()


def __generate_graphql_resources(codes_generated: dict, json: dict):
    """
    This method generate the code for the graphql resources.
    :param codes_generated: the code that will be generated.
    :param json: the json with the data.
    """
    codes_generated['code_generated/src/graphql/schema.graphql'] = generate_graphql_schema(json)
    codes_generated['code_generated/src/graphql/invoker.js'] = generator_invoker()


def __generate_dal_resources(codes_generated: dict, json: dict):
    """
    This method generate the resources for the dal.
    :param codes_generated: the code that will be generated.
    :param json: the json with the data.
    """
    __generate_models(codes_generated, json)
    __generate_event_parse_resources(codes_generated)
    __generate_dal_code(codes_generated, json)


def __generate_models(codes_generated: dict, json: dict):
    """
    This method generate the code for the models.
    :param codes_generated: the code that will be generated.
    :param json: the json with the data.
    """
    __generate_entities_model(codes_generated, json)
    __generate_links_model(codes_generated, json)


def __generate_entities_model(codes_generated: dict, json: dict):
    """
    This method generate the code for the model entity.
    :param codes_generated: the code that will be generated.
    :param json: the json with the data.
    """
    for entity in json['entities']:
        entity_name = generate_resource_name(entity)
        codes_generated[f'code_generated/src/model/{entity_name.lower()}.py'] = generate_model_entity(entity_name,
                                                                                                      entity['fields'])


def __generate_links_model(codes_generated: dict, json: dict):
    """
    This method generate the code for the model link.
    :param codes_generated: the code that will be generated.
    :param json: the json with the data.
    """
    for link in json['links']:
        link_name = generate_resource_name(link)
        codes_generated[f'code_generated/src/model/{link_name.lower()}.py'] = generate_model_link(link, json)


def __generate_event_parse_resources(code_generated: dict):
    """
    This method generate the code for the event resources.
    :param code_generated: the code that will be generated.
    """
    code_generated['code_generated/src/event/event_parse.py'] = generate_event_parse()
    code_generated['code_generated/src/event/event.py'] = generate_event_class()


def __generate_dal_code(codes_generated: dict, json: dict):
    """
    This method generate the code for the dal resources.
    :param codes_generated: the code that will be generated.
    :param json: the json with the data.
    """
    __generate_dynamo_manager_resources(codes_generated, json)
    codes_generated['code_generated/src/lambda.py'] = generation_one_file(json)


def __generate_dynamo_manager_resources(codes_generated: dict, json: dict):
    """
    This method generate the code for the dynamo manager resources.
    :param codes_generated: the code that will be generated.
    :param json: the json with the data.
    """
    __generate_utility_resources(codes_generated)
    codes_generated['code_generated/src/dynamo_manager/dynamo_manager.py'] = generate_dbmanager(json)
    codes_generated['code_generated/src/dynamo_manager/configuration.py'] = generate_configuration_class()


def __generate_utility_resources(codes_generated: dict):
    """
    This method generate the code for the utility resources.
    :param codes_generated: the code that will be generated.
    """
    codes_generated['code_generated/src/dynamo_manager/utility/utility.py'] = generate_utility_functions()
    codes_generated['code_generated/src/dynamo_manager/utility/exception_class.py'] = generator_exception()