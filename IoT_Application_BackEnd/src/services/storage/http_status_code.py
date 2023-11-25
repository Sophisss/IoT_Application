def ok(json_body=None):
    return __http_response(200, json_body)


def redirect(new_location: str):
    response = __http_response(302, None)
    headers = response.get("headers")
    headers["Location"] = new_location
    return response


def not_modified(json_body=None):
    return __http_response(304, json_body)


def forbidden(json_body=None):
    return __http_response(403, json_body)


def bad_request(json_body=None):
    return __http_response(400, json_body)


def not_found(json_body=None):
    return __http_response(404, json_body)


def internal_server_error(json_body=None):
    return __http_response(500, json_body)


def gone(json_body=None):
    return __http_response(410, json_body)


def __http_response(status_code: int, json_body):
    return {
        "statusCode": status_code,
        "body": json_body
    }
