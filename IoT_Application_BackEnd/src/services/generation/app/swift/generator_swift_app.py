from services.generation.app.swift.services.generator_error_service import generate_error_service
from services.generation.app.swift.services.generator_identity_client import generate_identity_client


def generate_swift_app(app_code: dict, json: dict) -> dict:
    """
    This method generate the code for swift app.
    :param app_code: the code that will be generated.
    :param json: the json with the data.
    :return: the code for swift app.
    """
    __generate_services(app_code, json)
    app_code = {f'swift/{key}': value for key, value in app_code.items()}
    return app_code


def __generate_services(app_code: dict, json: dict):
    """
    This method generate the code for the services.
    :param app_code: the code that will be generated.
    :param json: the json with the data.
    """
    app_code['src/services/ErrorsService.swift'] = generate_error_service()
    app_code['src/services/IdentityClient.swift'] = generate_identity_client()
