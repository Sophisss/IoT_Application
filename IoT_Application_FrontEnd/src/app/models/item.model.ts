import {Field} from "./field.model";

export class Item {
  ID: number;

  name: string;

  type: 'entity' | 'table' | 'link';

  table: string;

  partition_key: string;

  sort_key: string;

  first_item_ID: number;

  second_item_ID: number;

  numerosity: 'one-to-one' | 'one-to-many' | 'many-to-many' | 'many-to-one';

  fields: Field[];

  primary_key: string[];
}