/**
 * This model represents a field. ù
 * Each field can be composed of: name, type,
 * a variable that indicates whether the field is mandatory,
 * if the field is a string it can have the minimum and/or maximum length,
 * if the field is a number it can have the minimum and/or field or maximum
 * and can also have a list of allowed values.
 */
export class Field {

  name: String
  type: String
  required: Boolean
  minLength: Number | undefined
  maxLength: Number | undefined
  minimum: Number | undefined
  maximum: Number | undefined
  allowed_values: String[] = []

  constructor(name: String, type: String, required: Boolean) {
    this.name = name
    this.type = type
    this.required = required
  }

  setMinLength(minLenght: Number): void {
    this.minLength = minLenght;
  }

  setMaxLength(maxLength: Number): void {
    this.maxLength = maxLength;
  }

  setMinimum(minimum: Number): void {
    this.minimum = minimum;
  }

  setMaximum(maximum: Number): void {
    this.maximum = maximum;
  }
}
