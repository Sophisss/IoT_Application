export function request(ctx) {
  const { source, args } = ctx;
  return {
    operation: "Invoke",
    payload: { field: ctx.info.fieldName, arguments: args, source ,projection:ctx.info.selectionSetList},
  };
}

export function response(ctx) {
  return ctx.result;
}