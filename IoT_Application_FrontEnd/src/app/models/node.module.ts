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
  sort_key?: string;

  constructor(id: number, name: string, type: 'entity' | 'table', fields: Field[], table?: string, partition_key?: string, sort_key?: string) {
    this.id = id;
    this.name = name;
    this.type = type;
    this.fields = fields;
    this.table = (table === null || table === undefined) ? null : table;
    this.partition_key = (partition_key === null || partition_key === undefined) ? null : partition_key;
    this.sort_key = (sort_key === null || sort_key === undefined) ? null : sort_key;
    if ((this.type === 'entity' && this.table === null) || (this.type === 'table' && (this.partition_key === null || this.sort_key === null))) {
      throw new Error("The node is neither a table nor an entity");
    }
  }
}