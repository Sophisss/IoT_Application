def generate_utility() -> str:
    """
    This function generate the utility methods.
    :return: the utility methods generated.
    """
    return f"""{__generate_change_name_keys_method()}"""


def __generate_change_name_keys_method() -> str:
    """
    This function generate the change_name_keys method.
    :return: the change_name_keys method.
    """
    return """def change_name_keys(dict_to_change: dict, *args) -> dict:
    for key in args:
        dict_to_change[key[0]] = dict_to_change.pop(key[1])
    return dict_to_change"""