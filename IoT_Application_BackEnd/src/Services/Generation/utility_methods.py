import http_status_code


def generate_resource_name(resource):
    """
    This function generate the resource name.
    :param resource: The resource.
    :return: The resource name.
    """
    return resource.get("name") or f"{resource['first_entity']}{resource['second_entity']}"


def handle_response(response, success_message):
    """
    This function handles the API response and creates a standardized response.
    :param response: API response.
    :param success_message: Success message.
    :return: Standardized response.
    """
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    error_message = response.get('Error', {}).get('Message')

    if 200 <= status_code < 300:
        return http_status_code.ok(json_body=success_message)
    elif status_code == 403:
        return http_status_code.forbidden(json_body=error_message)
    elif status_code == 404:
        return http_status_code.not_found(json_body=error_message)
    elif 500 <= status_code < 500:
        return http_status_code.internal_server_error(json_body=error_message)
    else:
        return http_status_code.bad_request(json_body=error_message)


def check_response(response):
    """
    Check if the response is successful; if not, return the response.
    :param response: API response.
    :return: Response.
    """
    return response if response['statusCode'] != 200 else None
