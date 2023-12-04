import {Entity} from "./entity.model";
import {Field} from "./field.model";

/**
 * This model represents a link.
 * Each link is composed of two connecting entities and a list of fields.
 */
export class Link {
  id: number;

  name: string;

  first_entity: Entity;

  second_entity: Entity;

  fields: Field[] = []
}
