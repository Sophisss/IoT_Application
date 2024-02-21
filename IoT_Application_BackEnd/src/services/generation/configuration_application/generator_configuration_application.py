from services.generation.configuration_application.dal_resources.response_manager.generator_base_aws_service import \
    generate_base_aws_service
from services.generation.configuration_application.dal_resources.dynamo_manager.generator_dynamo_manager import \
    generate_dbmanager
from services.generation.configuration_application.dal_resources.dynamo_manager.project_dynamo_manager.generator_project_dynamo_manager import \
    generate_project_dynamo_manager
from services.generation.configuration_application.dal_resources.event_resources.generator_event_class import \
    generate_event_class
from services.generation.configuration_application.dal_resources.event_resources.generator_event_parse import \
    generate_event_parse
from services.generation.configuration_application.dal_resources.generator_utility import generate_utility
from services.generation.configuration_application.dal_resources.lambda_functions.generator_lambda_entity import \
    generate_lambda_entity
from services.generation.configuration_application.dal_resources.lambda_functions.generator_lambda_link import \
    generate_lambda_link
from services.generation.configuration_application.dal_resources.model.generator_model_entity import \
    generate_model_entity
from services.generation.configuration_application.dal_resources.model.generator_model_link import generate_model_link
from services.generation.configuration_application.dal_resources.response_manager.generator_exception import \
    generate_exception
from services.generation.configuration_application.dal_resources.response_manager.generator_response_manager import \
    generate_response_manager
from services.generation.configuration_application.generator_readme import generate_readme
from services.generation.configuration_application.generator_requirements import generate_requirements
from services.generation.configuration_application.graphql_resources.generator_invoker import generate_invoker
from services.generation.configuration_application.graphql_resources.schema.generator_schema import \
    generate_graphql_schema
from services.generation.configuration_application.template_resources.cognito.generator_cognito_template import \
    generate_cognito_template
from services.generation.configuration_application.template_resources.deployment_guide.generator_deployment_guide import \
    generate_deployment_guide
from services.generation.configuration_application.template_resources.api.generator_api_template import \
    generate_api_template
from services.generation.utility_methods import generate_resource_name
from services.generation.configuration_application.dal_resources.timeseries_manager.generator_timeseries_dal import \
    generate_timeseries_dal
from services.generation.configuration_application.dal_resources.iot_resources.generator_iot_base_models import *
from services.generation.configuration_application.dal_resources.timeseries_manager.generator_project_timeseries_manager import \
    generate_project_timeseries_manager
from services.generation.configuration_application.dal_resources.iot_resources.generator_iot_rules_app import \
    generate_iot_rules_app
from services.generation.configuration_application.template_resources.storage.generator_project_table import \
    generate_project_table
from services.generation.configuration_application.template_resources.telemetry.generator_telemetry_resources import \
    generate_telemetry_resources_template


def generate_code_configuration_application(json: dict) -> dict:
    """
    This method generate the code for the configuration application.
    :param json: the json with the data.
    :return: the code generated.
    """
    configuration_application_code = {'README.md': generate_readme(json['projectName'])}
    __generate_templates(configuration_application_code, json)
    __generate_deployment_guide(configuration_application_code)
    __generate_requirements(configuration_application_code)
    __generate_graphql_resources(configuration_application_code, json)
    __generate_models(configuration_application_code, json)
    __generate_response_manager(configuration_application_code)
    __generate_event_parse_resources(configuration_application_code, json)
    __generate_dal_resources(configuration_application_code, json)
    configuration_application_code = {f'configuration_application/{key}': value for key, value in
                                      configuration_application_code.items()}
    return configuration_application_code


def __generate_templates(configuration_application_code: dict, json: dict):
    """
    This method generate the code for the templates.
    :param configuration_application_code: the code that will be generated.
    :param json: the json with the data.
    """
    configuration_application_code['template/cognito.yaml'] = generate_cognito_template(
        json['awsConfig']['authentication']['cognito'])
    configuration_application_code['template/api.yaml'] = generate_api_template(json)
    configuration_application_code['template/application_storage.yaml'] = generate_project_table(json)
    configuration_application_code['template/iot_rules.yaml'] = generate_telemetry_resources_template(json)


def __generate_deployment_guide(configuration_application_code: dict):
    """
    This method generate the code for the deployment guide.
    :param configuration_application_code: the code that will be generated.
    """
    configuration_application_code['template/guide/deployment_guide.md'] = generate_deployment_guide()


def __generate_requirements(configuration_application_code: dict):
    """
    This method generate the code for the requirements.
    :param configuration_application_code: the code that will be generated.
    """
    configuration_application_code['src/requirements.txt'] = generate_requirements()


def __generate_graphql_resources(configuration_application_code: dict, json: dict):
    """
    This method generate the code for the graphql resources.
    :param configuration_application_code: the code that will be generated.
    :param json: the json with the data.
    """
    configuration_application_code['src/graphql/schema.graphql'] = generate_graphql_schema(json)
    configuration_application_code['src/graphql/invoker.js'] = generate_invoker()


def __generate_models(configuration_application_code: dict, json: dict):
    """
    This method generate the code for the models.
    :param configuration_application_code: the code that will be generated.
    :param json: the json with the data.
    """
    __generate_entities_model(configuration_application_code, json)
    __generate_links_model(configuration_application_code, json)


def __generate_entities_model(configuration_application_code: dict, json: dict):
    """
    This method generate the code for the model entity.
    :param configuration_application_code: the code that will be generated.
    :param json: the json with the data.
    """
    for entity in json['entities']:
        entity_name = generate_resource_name(entity)
        configuration_application_code[f'src/model/{entity_name.lower()}.py'] = generate_model_entity(entity_name,
                                                                                                      entity['fields'])


def __generate_links_model(configuration_application_code: dict, json: dict):
    """
    This method generate the code for the model link.
    :param configuration_application_code: the code that will be generated.
    :param json: the json with the data.
    """
    for link in json['links']:
        link_name = generate_resource_name(link)
        configuration_application_code[f'src/model/{link_name.lower()}.py'] = generate_model_link(link, json)


def __generate_response_manager(configuration_application_code: dict):
    """
    This method generate the code for the exception.
    :param configuration_application_code: the code that will be generated.
    """
    configuration_application_code['src/response_manager/base_aws_service.py'] = generate_base_aws_service()
    configuration_application_code['src/response_manager/exception_class.py'] = generate_exception()
    configuration_application_code['src/response_manager/response_manager.py'] = generate_response_manager()


def __generate_event_parse_resources(configuration_application_code: dict, json: dict):
    """
    This method generate the code for the event resources.
    :param configuration_application_code: the code that will be generated.
    """
    configuration_application_code['src/event/event_parse.py'] = generate_event_parse(json)
    configuration_application_code['src/event/event.py'] = generate_event_class()


def __generate_dal_resources(configuration_application_code: dict, json: dict):
    """
    This method generate the resources for the dal.
    :param configuration_application_code: the code that will be generated.
    :param json: the json with the data.
    """
    configuration_application_code['src/dynamo_manager/utility.py'] = generate_utility()
    __generate_dynamo_manager_resources(configuration_application_code, json)
    __generate_timeseries_manager_resources(configuration_application_code, json)
    __generate_iot_resources(configuration_application_code, json)
    __generate_lambdas_functions(configuration_application_code, json)


def __generate_dynamo_manager_resources(configuration_application_code: dict, json: dict):
    """
    This method generate the code for the dynamo manager resources.
    :param configuration_application_code: the code that will be generated.
    :param json: the json with the data.
    """
    configuration_application_code['src/dynamo_manager/dynamo_manager.py'] = generate_dbmanager()
    configuration_application_code[
        'src/dynamo_manager/project_dynamo_manager.py'] = generate_project_dynamo_manager(json)


def __generate_timeseries_manager_resources(configuration_application_code: dict, json: dict):
    """
    This method generate the code for the timeseries manager resources.
    :param configuration_application_code: the code that will be generated.
    :param json: the json with the data.
    """
    configuration_application_code['src/timestream_manager/timeseries_dal.py'] = generate_timeseries_dal()
    configuration_application_code[
        'src/timestream_manager/project_timeseries_manager.py'] = generate_project_timeseries_manager(json)


def __generate_iot_resources(configuration_application_code: dict, json: dict):
    """
    This method generate the code for the iot resources.
    :param configuration_application_code: the code that will be generated.
    :param json: the json with the data.
    """
    configuration_application_code['src/iot/device_status_change.py'] = generate_device_status_change()
    configuration_application_code['src/iot/device_status_event.py'] = generate_device_status_event()
    configuration_application_code['src/iot_rules_app.py'] = generate_iot_rules_app(json)


def __generate_lambdas_functions(configuration_application_code: dict, json: dict):
    """
    This method generate the code for the lambda functions.
    :param configuration_application_code: the code that will be generated.
    :param json: the json with the data.
    """
    __generate_lambdas_for_entities(configuration_application_code, json['entities'], json)
    __generate_lambdas_for_links(configuration_application_code, json['links'], json)


def __generate_lambdas_for_entities(configuration_application_code: dict, entities: dict, json: dict):
    """
    This method generate the code for the lambda functions for the entities.
    :param configuration_application_code: the code that will be generated.
    :param entities: the entities.
    :param json: the json with the data.
    """
    for entity in entities:
        entity_name = generate_resource_name(entity)
        configuration_application_code[f'src/lambda_{entity_name.lower()}.py'] = generate_lambda_entity(entity, json)


def __generate_lambdas_for_links(configuration_application_code: dict, links: dict, json: dict):
    """
    This method generate the code for the lambda functions for the links.
    :param configuration_application_code: the code that will be generated.
    :param links: the links.
    :param json: the json with the data.
    """
    for link in links:
        link_name = generate_resource_name(link)
        configuration_application_code[f'src/lambda_{link_name.lower()}.py'] = generate_lambda_link(link, json)
