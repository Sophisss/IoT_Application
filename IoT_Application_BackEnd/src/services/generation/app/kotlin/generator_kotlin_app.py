from services.generation.app.generator_amplify_config import generate_amplify_configuration
from services.generation.app.kotlin.models.generator_cloud_error import generate_cloud_error_model
from services.generation.app.kotlin.models.generator_model import generate_model
from services.generation.utility_methods import generate_resource_name


def generate_kotlin_app(json: dict) -> dict:
    """
    This method generate the code for kotlin app.
    :param json: the json with the data.
    :return: the code for kotlin app.
    """
    kotlin_app_code = {}
    __generate_amplify_configuration(kotlin_app_code)
    __generate_models(kotlin_app_code, json)
    kotlin_app_code = {f'kotlin/{key}': value for key, value in kotlin_app_code.items()}
    return kotlin_app_code


def __generate_amplify_configuration(kotlin_app_code: dict):
    """
    This method generate the amplify configuration.
    :param kotlin_app_code: the code that will be generated.
    """
    kotlin_app_code['raw/amplifyconfiguration.json'] = generate_amplify_configuration()


def __generate_models(kotlin_app_code: dict, json: dict):
    """
    This method generate the models for kotlin app.
    :param kotlin_app_code: the code that will be generated.
    :param json: the json with the data.
    :return: the models for kotlin app.
    """
    kotlin_app_code['models/CloudError.kt'] = generate_cloud_error_model()
    for item in json['entities']:
        item_name = generate_resource_name(item)
        kotlin_app_code[f'models/{item_name}.kt'] = generate_model(item, item_name)
