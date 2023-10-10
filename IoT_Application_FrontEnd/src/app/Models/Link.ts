import {Field} from "./Field";

export class Link {

  first_entity: String;

  second_entity: String

  fields: Field[] = []

  constructor(first_entity: String, second_entity: String) {
    this.first_entity = first_entity
    this.second_entity = second_entity
  }
}
