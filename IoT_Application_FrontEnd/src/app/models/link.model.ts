import {Field} from "./field.model";

/**
 * This model represents a link.
 * Each link is composed of two connecting entities and a list of fields.
 */
export class Link {
  id: number;
  name: string;
  first_entity: string;
  second_entity: string;
  fields: Field[];
  type: 'link';

  constructor(id: number, name: string, first_entity: string, second_entity: string, fields: Field[]) {
    this.id = id;
    this.name = name;
    this.first_entity = first_entity;
    this.second_entity = second_entity;
    this.fields = fields;
  }
}
