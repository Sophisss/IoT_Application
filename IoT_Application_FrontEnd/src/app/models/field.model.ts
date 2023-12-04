/**
 * This model represents a field. ù
 * Each field can be composed of: name, type,
 * a variable that indicates whether the field is mandatory,
 * if the field is a string it can have the minimum and/or maximum length,
 * if the field is a number it can have the minimum and/or field or maximum
 * and can also have a list of allowed values.
 */
export class Field {

  name: string
  type: string
  required: Boolean
  minLength: number | undefined
  maxLength: number | undefined
  minimum: number | undefined
  maximum: number | undefined
  allowed_values: string[] = []
}
