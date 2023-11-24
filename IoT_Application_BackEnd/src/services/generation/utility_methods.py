def generate_resource_name(resource):
    """
    This function generate the resource name.
    :param resource: The resource.
    :return: The resource name.
    """
    return resource.get("name") or f"{resource['first_entity']}{resource['second_entity']}"
