import {Field} from "./Field";

/**
 * This model represents an entity. 
 * Each entity is characterized by a name, 
 * an id and a list of fields.
 */
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
