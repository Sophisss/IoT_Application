import { Entity } from "./Entity";
import {Field} from "./Field";

export class Link {

  first_entity: Entity;

  second_entity: Entity

  fields: Field[] = []

  constructor(first_entity: Entity, second_entity: Entity) {
    this.first_entity = first_entity
    this.second_entity = second_entity
  }
}
