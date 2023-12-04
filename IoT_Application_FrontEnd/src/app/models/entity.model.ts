import {Field} from "./field.model";

/**
 * This model represents an entity.
 * Each entity is characterized by a name,
 * an id and a list of fields.
 */
export class Entity {

  id: number;

  name: string;

  table: string | undefined;

  fields: Field[] = [];
}
