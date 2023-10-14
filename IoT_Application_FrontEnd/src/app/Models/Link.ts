import { Entity } from "./Entity";
import {Field} from "./Field";

/**
 * This model represents a link. 
 * Each link is composed of two connecting entities and a list of fields.
 */
export class Link {

  first_entity: Entity;

  second_entity: Entity

  fields: Field[] = []

  constructor(first_entity: Entity, second_entity: Entity) {
    this.first_entity = first_entity
    this.second_entity = second_entity
  }
}
