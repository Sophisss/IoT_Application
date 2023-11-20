def generator_invoker():
    """
    This function generates the invoker file for the lambda function.
    :return: The invoker file.
    """
    return f"""import {{util}} from "@aws-appsync/utils";
{generate_request()}
{generate_response()}
"""


def generate_request():
    """
    This function generates the request function for the invoker file.
    :return: The request function.
    """
    return """
export function request(ctx) {{
    const {{source, args}} = ctx;
    return {{
        operation: "Invoke",
        payload: {{field: ctx.info.fieldName, arguments: args, source, projection: ctx.info.selectionSetList}},
    }};
}}"""


def generate_response():
    """
    This function generates the response function for the invoker file.
    :return: The response function.
    """
    return """
export function response(ctx) {{
    const {{result}} = ctx
    const errors = ctx.result?.errors;
    if (errors !== undefined){{
        return util.error(errors.message,errors.type)
    }}
    return result;
}}"""