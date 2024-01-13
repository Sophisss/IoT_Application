from services.generation.app.swift.generator_swift_app import generate_swift_app


def generate_app(json: dict) -> dict:
    """
    This method generate the code for the app.
    :param json: the json with the data.
    :return: the app code generated.
    """
    app_code = {}
    app_code.update(generate_swift_app(json))
    app_code = {f'app/{key}': value for key, value in app_code.items()}
    return app_code
