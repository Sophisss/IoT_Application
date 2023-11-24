import {Field} from "./Field";

/**
 * This model represents an entity.
 * Each entity is characterized by a name,
 * an id and a list of fields.
 */
export class Entity {

  id: Number;

  name: String;

  table: String | undefined;

  fields: Field[] = [];

  constructor(id: Number, entity_name: String) {
    this.name = entity_name
    this.id = id
  }

  setTable(table_name: String): void {
    this.table = table_name;
  }


  resetTable() {
    this.table = undefined
  }
}
