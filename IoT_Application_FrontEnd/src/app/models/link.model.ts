import {Entity} from "./entity.model";
import {Field} from "./field.model";

/**
 * This model represents a link.
 * Each link is composed of two connecting entities and a list of fields.
 */
export class Link {

  first_entity: Entity;

  second_entity: Entity;

  fields: Field[] = []

  constructor(first_entity: Entity, second_entity: Entity) {
    this.first_entity = first_entity
    this.second_entity = second_entity
  }
}
