/**
 * This model represents a field, each characterized by:
 * name: the name of the field;
 * type: the type of the field;
 * required: a variable that indicates whether the field is mandatory;
 * minLength: if the field is a string it can have a minimum length;
 * maxLength: if the field is a string it can have a maximum length;
 * minimum: if the field is a number it can have a minimum value;
 * maximum: if the field is a number it can have a maximum value;
 * allowed_values: if the field is a string it can have a list of allowed values.
 */
export class Field {

  name: string
  type: string
  required: boolean
  minLength?: number | undefined
  maxLength?: number | undefined
  minimum?: number | undefined
  maximum?: number | undefined
  allowedValues?: string[] | undefined
}
