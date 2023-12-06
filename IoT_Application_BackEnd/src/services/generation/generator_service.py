from services.generation.dal.dynamo_manager.generator_base_aws_service import generate_base_aws_service
from services.generation.dal.dynamo_manager.generator_dynamo_manager import generate_dbmanager
from services.generation.dal.dynamo_manager.project_dynamo_manager.generator_project_dynamo_manager import generator_project_dynamo_manager
from services.generation.dal.event.generator_event_class import generate_event_class
from services.generation.dal.event.generator_event_parse import generate_event_parse
from services.generation.dal.generator_utility import generate_utility
from services.generation.dal.lambda_functions.generate_lambda_entity import generate_lambda_entity
from services.generation.dal.lambda_functions.generate_lambda_link import generate_lambda_link
from services.generation.dal.model.generate_model_entity import generate_model_entity
from services.generation.dal.model.generate_model_link import generate_model_link
from services.generation.dal.response_manager.generator_exception import generator_exception
from services.generation.dal.response_manager.generator_response_manager import generate_response_manager
from services.generation.deployment_guide.generator_deployment_guide import generate_deployment_guide
from services.generation.generator_readme import generate_readme
from services.generation.graphql_resources.generate_invoker import generator_invoker
from services.generation.graphql_resources.schema.generate_schema import generate_graphql_schema
from services.generation.requirements.generator_requirements import generate_requirements
from services.generation.templates.cognito.generator_cognito_template import generate_cognito_template
from services.generation.templates.generator_api_template import generate_api_template
from services.generation.utility_methods import generate_resource_name


def generate_code(json: dict) -> dict:
    """
    This function generate the code.
    :param json: the json containing the data.
    :return: the code generated.
    """
    code_generated = {'README.md': generate_readme(json['projectName'])}
    __generate_templates(code_generated, json)
    __generate_deployment_guide(code_generated)
    __generate_requirements(code_generated)
    __generate_graphql_resources(code_generated, json)
    __generate_models(code_generated, json)
    __generate_response_manager(code_generated)
    __generate_event_parse_resources(code_generated, json)
    __generate_dal_resources(code_generated, json)
    code_generated = {f'code_generated/{key}': value for key, value in code_generated.items()}
    return code_generated


def __generate_templates(codes_generated: dict, json: dict):
    """
    This method generate the code for the templates.
    :param codes_generated: the code that will be generated.
    :param json: the json with the data.
    """
    codes_generated['template/cognito.yaml'] = generate_cognito_template(json['awsConfig']['authentication']['cognito'])
    codes_generated['template/api.yaml'] = generate_api_template(json)


def __generate_deployment_guide(codes_generated: dict):
    """
    This method generate the code for the deployment guide.
    :param codes_generated: the code that will be generated.
    """
    codes_generated['template/guide/deployment_guide.md'] = generate_deployment_guide()


def __generate_requirements(codes_generated: dict):
    """
    This method generate the code for the requirements.
    :param codes_generated: the code that will be generated.
    """
    codes_generated['src/requirements.txt'] = generate_requirements()


def __generate_graphql_resources(codes_generated: dict, json: dict):
    """
    This method generate the code for the graphql resources.
    :param codes_generated: the code that will be generated.
    :param json: the json with the data.
    """
    codes_generated['src/graphql/schema.graphql'] = generate_graphql_schema(json)
    codes_generated['src/graphql/invoker.js'] = generator_invoker()


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
        codes_generated[f'src/model/{entity_name.lower()}.py'] = generate_model_entity(entity_name, entity['fields'])


def __generate_links_model(codes_generated: dict, json: dict):
    """
    This method generate the code for the model link.
    :param codes_generated: the code that will be generated.
    :param json: the json with the data.
    """
    for link in json['links']:
        link_name = generate_resource_name(link)
        codes_generated[f'src/model/{link_name.lower()}.py'] = generate_model_link(link, json)


def __generate_response_manager(codes_generated: dict):
    """
    This method generate the code for the exception.
    :param codes_generated: the code that will be generated.
    """
    codes_generated['src/dal/response_manager/exception_class.py'] = generator_exception()
    codes_generated['src/dal/response_manager/response_manager.py'] = generate_response_manager()


def __generate_event_parse_resources(code_generated: dict, json: dict):
    """
    This method generate the code for the event resources.
    :param code_generated: the code that will be generated.
    """
    code_generated['src/event/event_parse.py'] = generate_event_parse(json)
    code_generated['src/event/event.py'] = generate_event_class()


def __generate_dal_resources(codes_generated: dict, json: dict):
    """
    This method generate the resources for the dal.
    :param codes_generated: the code that will be generated.
    :param json: the json with the data.
    """
    codes_generated['src/dal/utility.py'] = generate_utility()
    __generate_dynamo_manager_resources(codes_generated, json)
    __generate_lambdas_functions(codes_generated, json)


def __generate_dynamo_manager_resources(codes_generated: dict, json: dict):
    """
    This method generate the code for the dynamo manager resources.
    :param codes_generated: the code that will be generated.
    :param json: the json with the data.
    """
    codes_generated['src/dal/dynamo_manager/base_aws_service.py'] = generate_base_aws_service()
    codes_generated['src/dal/dynamo_manager/dynamo_manager.py'] = generate_dbmanager()
    codes_generated['src/dal/dynamo_manager/project_dynamo_manager.py'] = generator_project_dynamo_manager(json)


def __generate_lambdas_functions(codes_generated: dict, json: dict):
    """
    This method generate the code for the lambda functions.
    :param codes_generated: the code that will be generated.
    :param json: the json with the data.
    """
    __generate_lambdas_for_entities(codes_generated, json['entities'], json)
    __generate_lambdas_for_links(codes_generated, json['links'], json)


def __generate_lambdas_for_entities(codes_generated: dict, entities: dict, json: dict):
    """
    This method generate the code for the lambda functions for the entities.
    :param codes_generated: the code that will be generated.
    :param entities: the entities.
    :param json: the json with the data.
    """
    for entity in entities:
        entity_name = generate_resource_name(entity)
        codes_generated[f'src/lambda_{entity_name.lower()}.py'] = generate_lambda_entity(entity, json)


def __generate_lambdas_for_links(codes_generated: dict, links: dict, json: dict):
    """
    This method generate the code for the lambda functions for the links.
    :param codes_generated: the code that will be generated.
    :param links: the links.
    :param json: the json with the data.
    """
    for link in links:
        link_name = generate_resource_name(link)
        codes_generated[f'src/lambda_{link_name.lower()}.py'] = generate_lambda_link(link, json)
