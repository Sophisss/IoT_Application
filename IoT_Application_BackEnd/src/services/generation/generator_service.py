from services.generation.configuration_application.generator_configuration_application import \
    generate_code_configuration_application


def generate_code(json: dict) -> dict:
    """
    This function generate the code.
    :param json: the json containing the data.
    :return: the code generated.
    """
    code_generated = {}
    code_generated.update(generate_code_configuration_application(code_generated, json))
    # code_generated.update(generate_app(code_generated, json))
    return code_generated
