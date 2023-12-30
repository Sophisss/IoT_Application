from services.generation.app.generator_app import generate_app
from services.generation.configuration_application.generator_configuration_application import \
    generate_code_configuration_application


def generate_code(json: dict) -> dict:
    """
    This function generates the code for the application.
    :param json: the json with the information of the application.
    :return: the code generated.
    """
    code_generated = {}
    code_generated.update(generate_code_configuration_application(json))
    code_generated.update(generate_app(json))
    return code_generated
