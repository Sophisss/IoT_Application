export class Item {
  ID: number;

  name: string;

  type: 'entity' | 'table' | 'link';

  table: string;

  partition_key: string;

  sort_key: string;

  first_item: string;

  second_item: string;

}