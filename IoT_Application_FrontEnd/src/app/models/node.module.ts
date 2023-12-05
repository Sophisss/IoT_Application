import {Field} from "./field.model";

/**
 * This model represents a node of the diagram.
 * Each entity is characterized by a name, an id, a type and a list of fields.
 * The type is used to distinguish between entities and tables.
 */
export class DiagramNode {
  id: number;

  name: string;

  fields: Field[] = [];

  type: 'entity' | 'table';

  table?: string;

  partition_key?: string;

  sort_Key?: string;
}