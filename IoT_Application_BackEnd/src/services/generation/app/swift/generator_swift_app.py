from services.generation.app.generator_amplify_config import generate_amplify_configuration
from services.generation.app.swift.services.generator_error_service import generate_error_service
from services.generation.app.swift.services.generator_identity_client import generate_identity_client


def generate_swift_app(json: dict) -> dict:
    """
    This method generate the code for swift app.
    :param json: the json with the data.
    :return: the code for swift app.
    """
    swift_app_code = {}
    __generate_amplify_configuration(swift_app_code)
    __generate_services(swift_app_code, json)
    swift_app_code = {f'swift/{key}': value for key, value in swift_app_code.items()}
    return swift_app_code


def __generate_amplify_configuration(swift_app_code: dict):
    """
    This method generate the amplify configuration.
    :param swift_app_code: the code that will be generated.
    """
    swift_app_code['amplify_config/amplifyconfiguration.json'] = generate_amplify_configuration()


def __generate_services(swift_app_code: dict, json: dict):
    """
    This method generate the code for the services.
    :param swift_app_code: the code that will be generated.
    :param json: the json with the data.
    """
    swift_app_code['src/services/ErrorsService.swift'] = generate_error_service()
    swift_app_code['src/services/IdentityClient.swift'] = generate_identity_client()
