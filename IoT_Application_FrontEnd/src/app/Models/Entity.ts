import {Field} from "./Field";

export class Entity {

  entity_id : Number

  entity_name: String;

  fields: Field[] = [];

  table_name !: String

  constructor(id: Number, entity_name: String) {
    this.entity_name = entity_name
    this.entity_id = id
  }
}
