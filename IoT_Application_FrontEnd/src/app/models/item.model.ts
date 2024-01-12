import {Field} from "./field.model";

export class Item {
  ID: number;

  name: string;

  type: 'entity' | 'table' | 'link';

  table: string;

  partition_key_name: string;

  partition_key_type: 'string' | 'integer';

  sort_key_name: string;

  sort_key_type: 'string' | 'integer'

  first_item_ID: number;

  second_item_ID: number;

  numerosity: 'one-to-one' | 'one-to-many' | 'many-to-many' | 'many-to-one';

  fields: Field[];

  primary_key: string[];

  keyword: string;

  separator: string;
}