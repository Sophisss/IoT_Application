import {Field} from "./field.model";

export class Item {
  ID: number;

  name: string;

  type: 'entity' | 'table' | 'link';

  table: string;

  partition_key: string;

  sort_key: string;

  first_item: string;

  second_item: string;

  fields: Field[] = [
    {
      name: 'Field 1',
      type: 'text',
      required: true
    },
    {
      name: 'Field 2',
      type: 'number',
      required: true
    },
  ];
}