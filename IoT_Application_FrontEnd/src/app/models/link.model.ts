import {Field} from "./field.model";
import {DiagramNode} from "./node.module";

/**
 * This model represents a link.
 * Each link is composed of two connecting entities and a list of fields.
 */
export class Link {
  id: number;

  name: string;

  first_entity: DiagramNode;

  second_entity: DiagramNode;

  fields: Field[] = []
}
