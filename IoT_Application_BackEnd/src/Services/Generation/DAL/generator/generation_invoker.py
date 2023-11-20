def generator_invoker():
    return f"""
import {{util}} from "@aws-appsync/utils";

export function request(ctx) {{
    const {{source, args}} = ctx;
    return {{
        operation: "Invoke",
        payload: {{field: ctx.info.fieldName, arguments: args, source, projection: ctx.info.selectionSetList}},
    }};
}}

export function response(ctx) {{
    const {{result}} = ctx
    const errors = ctx.result?.errors;
    if (errors !== undefined){{
        return util.error(errors.message,errors.type)
    }}
    return result;
}}
"""
