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
  allowed_values?: string[] = []

  constructor(name: string, type: string, required: boolean, minLength?: number, maxLength?: number, minimum?: number, maximum?: number, allowed_values?: string[]) {
    this.name = name
    this.type = type
    this.required = required
    this.minLength = (minLength === null || minLength === undefined) ? null : minLength;
    this.maxLength = (maxLength === null || maxLength === undefined) ? null : maxLength;
    this.minimum = (minimum === null || minimum === undefined) ? null : minimum;
    this.maximum = (maximum === null || maximum === undefined) ? null : maximum;
    this.allowed_values = (allowed_values === null || allowed_values === undefined) ? null : allowed_values;
    if (this.notAString() && this.notANumber() && this.type !== 'boolean') {
      throw new Error("The field is neither a string nor a number");
    }
  }

  notANumber(): boolean {
    return (this.minimum === null || this.maximum === null) && this.type !== 'number';
  }

  notAString(): boolean {
    return (this.minLength === null || this.maxLength === null) && this.type !== 'string';
  }
}
