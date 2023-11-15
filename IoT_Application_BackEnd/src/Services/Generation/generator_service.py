from Services.Generation.DAL.generator_lambda_service import generate_lambda_code


def generate_code(json: dict) -> list[str]:
    """
    This function generate the code.
    :param json: the json with the data.
    :return: the code generated.
    """
    codes_generated = []
    codes_generated.append(generate_lambda_code(json))
    return codes_generated
