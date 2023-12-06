def generate_utility() -> str:
    """
    This function generate the utility methods.
    :return: the utility methods generated.
    """
    return f"""{__generate_change_name_keys_method()}
{__generate_remove_null_values_method()}"""


def __generate_change_name_keys_method() -> str:
    """
    This function generate the change_name_keys method.
    :return: the change_name_keys method.
    """
    return """def change_name_keys(dict_to_change: dict, *args):
    if isinstance(dict_to_change, list):
        return [change_name_keys(item, *args) for item in dict_to_change]

    for new_key, old_key, separator in args:
        if old_key in dict_to_change:
            value = dict_to_change.pop(old_key)
            dict_to_change[new_key] = value.split(separator)[1]

    return dict_to_change
    """


def __generate_remove_null_values_method() -> str:
    """
    This function generates the function used to remove null values from a dictionary.
    :return: The function used to remove null values from a dictionary.
    """
    return """
def remove_null_values(dictionary: dict) -> dict:
    return {
        key: remove_null_values(value) if isinstance(value, dict) else value
        for key, value in dictionary.items()
        if value is not None
    }
    """